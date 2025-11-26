"""Main LangGraph workflow for general contract drafting."""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.models.contract_drafting_state import ContractDraftingState
from src.nodes.contract_drafting import (
    user_input_handler_node,
    knowledge_base_fetcher_node,
    structure_analyzer_node,
    content_mapper_node,
    clause_generator_node,
    consistency_checker_node,
    quality_reviewer_node,
    output_formatter_node,
)

# Reuse existing extractors
from src.nodes import (
    document_extractor_node,
    excel_extractor_node,
)


def create_contract_drafting_graph():
    """
    Create the general contract drafting workflow graph.

    Flow:
    1. User Input Handler - Process user inputs and load contract type
    2. Document Extractors (parallel) - Extract from PDF/DOCX and Excel
    3. Knowledge Base Fetcher - Get historical contracts/clauses (can fail gracefully)
    4. Structure Analyzer - Build contract outline
    5. Content Mapper - Map extracted data to sections
    6. Clause Generator - Generate contract sections
    7. Consistency Checker - Validate consistency
    8. Quality Reviewer - Assess quality
    9. Output Formatter - Generate final files

    Returns:
        Compiled LangGraph workflow
    """
    print("🔧 Building contract drafting workflow...")

    # Initialize the graph
    graph = StateGraph(ContractDraftingState)

    # Add all nodes
    graph.add_node("user_input_handler", user_input_handler_node)
    graph.add_node("document_extractor", document_extractor_node)
    graph.add_node("excel_extractor", excel_extractor_node)
    graph.add_node("knowledge_base_fetcher", knowledge_base_fetcher_node)
    graph.add_node("structure_analyzer", structure_analyzer_node)
    graph.add_node("content_mapper", content_mapper_node)
    graph.add_node("clause_generator", clause_generator_node)
    graph.add_node("consistency_checker", consistency_checker_node)
    graph.add_node("quality_reviewer", quality_reviewer_node)
    graph.add_node("output_formatter", output_formatter_node)

    # Define the flow
    graph.add_edge(START, "user_input_handler")
    graph.add_edge("user_input_handler", "document_extractor")
    graph.add_edge("document_extractor", "excel_extractor")
    graph.add_edge("excel_extractor", "knowledge_base_fetcher")
    graph.add_edge("knowledge_base_fetcher", "structure_analyzer")
    graph.add_edge("structure_analyzer", "content_mapper")
    graph.add_edge("content_mapper", "clause_generator")
    graph.add_edge("clause_generator", "consistency_checker")
    graph.add_edge("consistency_checker", "quality_reviewer")
    graph.add_edge("quality_reviewer", "output_formatter")
    graph.add_edge("output_formatter", END)

    # Compile the graph with memory for checkpointing
    memory = MemorySaver()
    compiled_graph = graph.compile(checkpointer=memory)

    print("✓ Contract drafting workflow built successfully")

    return compiled_graph


if __name__ == "__main__":
    # Test graph creation
    graph = create_contract_drafting_graph()
    print("\n✓ Graph created successfully!")
    print("  Nodes:", list(graph.nodes.keys()) if hasattr(graph, 'nodes') else "N/A")
