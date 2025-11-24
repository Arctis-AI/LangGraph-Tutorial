"""Main LangGraph workflow for contract generation."""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.models.state import ContractState
from src.nodes import (
    upload_handler_node,
    document_classifier_node,
    pdf_extractor_node,
    excel_extractor_node,
    data_validator_node,
    data_merger_node,
    contract_generator_node,
    quality_checker_node,
    output_formatter_node
)
from src.nodes.document_classifier import route_documents
from src.nodes.quality_checker import quality_check_router


def create_contract_graph():
    """
    Create the contract generation workflow graph.
    """
    print("🔧 Building contract generation workflow...")

    # Initialize the graph
    graph = StateGraph(ContractState)

    # Add all nodes
    graph.add_node("upload_handler", upload_handler_node)
    graph.add_node("document_classifier", document_classifier_node)
    graph.add_node("pdf_extractor", pdf_extractor_node)
    graph.add_node("excel_extractor", excel_extractor_node)
    graph.add_node("data_validator", data_validator_node)
    graph.add_node("data_merger", data_merger_node)
    graph.add_node("contract_generator", contract_generator_node)
    graph.add_node("quality_checker", quality_checker_node)
    graph.add_node("output_formatter", output_formatter_node)

    # Define the flow
    # Start -> Upload Handler
    graph.add_edge(START, "upload_handler")

    # Upload Handler -> Document Classifier
    graph.add_edge("upload_handler", "document_classifier")

    # Document Classifier -> Conditional routing to extractors
    # For simplicity, we'll run both extractors in sequence if both documents are available
    graph.add_edge("document_classifier", "pdf_extractor")
    graph.add_edge("pdf_extractor", "excel_extractor")

    # Extractors -> Data Validator
    graph.add_edge("excel_extractor", "data_validator")

    # Data Validator -> Data Merger
    graph.add_edge("data_validator", "data_merger")

    # Data Merger -> Contract Generator
    graph.add_edge("data_merger", "contract_generator")

    # Contract Generator -> Quality Checker
    graph.add_edge("contract_generator", "quality_checker")

    # Quality Checker -> Output Formatter (simplified - always pass for POC)
    graph.add_edge("quality_checker", "output_formatter")

    # Output Formatter -> End
    graph.add_edge("output_formatter", END)

    # Compile the graph with memory for checkpointing
    memory = MemorySaver()
    compiled_graph = graph.compile(checkpointer=memory)

    return compiled_graph


def create_contract_graph_with_routing():
    """
    Create the contract generation workflow with conditional routing.
    This is a more complex version that handles different document availability scenarios.
    """
    print("🔧 Building advanced contract generation workflow...")

    # Initialize the graph
    graph = StateGraph(ContractState)

    # Add all nodes
    graph.add_node("upload_handler", upload_handler_node)
    graph.add_node("document_classifier", document_classifier_node)
    graph.add_node("pdf_extractor", pdf_extractor_node)
    graph.add_node("excel_extractor", excel_extractor_node)
    graph.add_node("data_validator", data_validator_node)
    graph.add_node("data_merger", data_merger_node)
    graph.add_node("contract_generator", contract_generator_node)
    graph.add_node("quality_checker", quality_checker_node)
    graph.add_node("output_formatter", output_formatter_node)
    graph.add_node("error_handler", error_handler_node)

    # Define the flow
    graph.add_edge(START, "upload_handler")
    graph.add_edge("upload_handler", "document_classifier")

    # Conditional routing based on available documents
    def route_from_classifier(state):
        status = state.get("processing_status", "")
        if status == "both_documents":
            return "pdf_extractor"
        elif status == "pdf_only":
            return "pdf_extractor"
        elif status == "excel_only":
            return "excel_extractor"
        else:
            return "error_handler"

    graph.add_conditional_edges(
        "document_classifier",
        route_from_classifier,
        {
            "pdf_extractor": "pdf_extractor",
            "excel_extractor": "excel_extractor",
            "error_handler": "error_handler"
        }
    )

    # Handle extraction flow
    def route_after_pdf(state):
        status = state.get("processing_status", "")
        if status == "both_documents":
            return "excel_extractor"
        else:
            return "data_validator"

    graph.add_conditional_edges(
        "pdf_extractor",
        route_after_pdf,
        {
            "excel_extractor": "excel_extractor",
            "data_validator": "data_validator"
        }
    )

    graph.add_edge("excel_extractor", "data_validator")
    graph.add_edge("data_validator", "data_merger")
    graph.add_edge("data_merger", "contract_generator")
    graph.add_edge("contract_generator", "quality_checker")

    # Quality check routing
    graph.add_conditional_edges(
        "quality_checker",
        quality_check_router,
        {
            "pass": "output_formatter",
            "fail": "output_formatter"  # For POC, always proceed
        }
    )

    graph.add_edge("output_formatter", END)
    graph.add_edge("error_handler", END)

    # Compile the graph
    memory = MemorySaver()
    compiled_graph = graph.compile(checkpointer=memory)

    return compiled_graph


def error_handler_node(state: ContractState):
    """Handle errors in the workflow."""
    return {
        "messages": [{
            "role": "system",
            "content": f"❌ Workflow error: {state.get('error', 'Unknown error')}"
        }],
        "processing_status": "error"
    }