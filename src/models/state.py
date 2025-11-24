"""State definition for LangGraph contract generation workflow."""

from typing import Dict, List, Optional, Any, Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class ContractState(TypedDict):
    """State for the contract generation workflow."""

    # Messages for conversation history
    messages: Annotated[list, add_messages]

    # File handling
    uploaded_files: Dict[str, str]  # {file_type: file_path}
    pdf_path: Optional[str]
    excel_path: Optional[str]

    # Extracted raw data
    verhandlungsprotokoll_raw: Optional[str]  # Raw text from PDF
    leistungsverzeichnis_raw: Optional[List[Dict[str, Any]]]  # Raw data from Excel

    # Structured extracted data
    verhandlungsprotokoll_data: Optional[Dict[str, Any]]
    leistungsverzeichnis_data: Optional[List[Dict[str, Any]]]

    # Processing data
    merged_data: Optional[Dict[str, Any]]
    contract_draft: Optional[str]
    formatted_contract: Optional[str]

    # Validation and quality
    validation_errors: List[str]
    validation_passed: bool
    quality_report: Optional[Dict[str, Any]]
    quality_passed: bool

    # Metadata
    processing_status: str
    current_step: str
    output_path: Optional[str]

    # Error handling
    error: Optional[str]
    retry_count: int