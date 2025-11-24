"""Document classifier node to route documents to appropriate extractors."""

from typing import Dict, Any, Literal
from src.models.state import ContractState


def document_classifier_node(state: ContractState) -> Dict[str, Any]:
    """
    Classify uploaded documents and determine extraction route.
    """
    print("🔍 Classifying documents...")

    updates = {
        "current_step": "document_classifier",
        "messages": []
    }

    # Check which files are available
    has_pdf = state.get("pdf_path") is not None
    has_excel = state.get("excel_path") is not None

    if has_pdf and has_excel:
        updates["processing_status"] = "both_documents"
        updates["messages"].append({
            "role": "system",
            "content": "✓ Both Verhandlungsprotokoll and Leistungsverzeichnis available"
        })
    elif has_pdf:
        updates["processing_status"] = "pdf_only"
        updates["messages"].append({
            "role": "system",
            "content": "ℹ️ Only Verhandlungsprotokoll available - will generate limited contract"
        })
    elif has_excel:
        updates["processing_status"] = "excel_only"
        updates["messages"].append({
            "role": "system",
            "content": "ℹ️ Only Leistungsverzeichnis available - will generate limited contract"
        })
    else:
        updates["processing_status"] = "no_documents"
        updates["error"] = "No documents available for processing"
        updates["messages"].append({
            "role": "system",
            "content": "❌ No documents available for processing"
        })

    return updates


def route_documents(state: ContractState) -> Literal["pdf_extractor", "excel_extractor", "both", "error"]:
    """
    Routing function to determine which extractors to run.
    """
    status = state.get("processing_status", "")

    if status == "both_documents":
        return "both"
    elif status == "pdf_only":
        return "pdf_extractor"
    elif status == "excel_only":
        return "excel_extractor"
    else:
        return "error"