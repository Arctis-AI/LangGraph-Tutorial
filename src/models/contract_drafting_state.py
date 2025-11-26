"""State definition for general contract drafting workflow."""

from typing import Dict, List, Optional, Any, Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from datetime import datetime


def merge_steps(left: str, right: str) -> str:
    """Reducer for current_step: joins multiple steps with ' + '."""
    if not left:
        return right
    if not right:
        return left
    # Merge parallel steps
    steps = set(left.split(" + ")) | set(right.split(" + "))
    return " + ".join(sorted(steps))


class ContractDraftingState(TypedDict):
    """State for the general contract drafting workflow."""

    # ===== [1] User Inputs =====
    contract_type_id: str
    contract_type_code: str  # e.g., "SITE_SUPERVISION"
    contract_type_data: Dict[str, Any]  # Full contract type object from JSON
    project_description: str
    uploaded_documents: List[Dict[str, str]]

    # ===== [2] Extracted Data =====
    verhandlungsprotokoll_data: Optional[Dict[str, Any]]
    leistungsverzeichnis_data: Optional[Dict[str, Any]]
    verhandlungsprotokoll_raw: Optional[str]
    leistungsverzeichnis_raw: Optional[List[Dict[str, Any]]]

    # For backward compatibility with existing extractors
    pdf_path: Optional[str]
    excel_path: Optional[str]

    # ===== [3] Knowledge Base Data (fetched from Supabase) =====
    retrieved_contracts: List[Dict[str, Any]]  # Similar contracts
    retrieved_clauses: List[Dict[str, Any]]    # Example clauses
    contract_structures: List[Dict[str, Any]]  # Structure examples

    # ===== [4] Structure =====
    contract_outline: List[Dict[str, Any]]  # Hierarchical outline

    # ===== [5] Content Mapping =====
    section_mappings: Dict[str, Dict[str, Any]]  # Data → Sections

    # ===== [6] Generation =====
    generated_sections: Dict[str, str]  # Section number → text
    contract_draft: str  # Full contract text

    # ===== [7] Consistency =====
    consistency_issues: List[Dict[str, Any]]

    # ===== [8] Quality =====
    quality_report: Dict[str, Any]
    quality_score: float
    quality_passed: bool

    # ===== [9] Output =====
    output_files: Dict[str, str]
    output_path: Optional[str]

    # ===== Status & Logging =====
    current_step: Annotated[str, merge_steps]  # Supports parallel updates
    processing_status: str
    messages: Annotated[list, add_messages]
    errors: Annotated[List[str], lambda x, y: x + y]  # Concatenate errors from parallel nodes

    # ===== Metadata =====
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
