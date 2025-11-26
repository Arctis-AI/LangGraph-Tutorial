"""Content mapper node for mapping extracted data to contract sections."""

from typing import Dict, Any
from src.models.contract_drafting_state import ContractDraftingState


def content_mapper_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Map extracted data to contract sections.

    Analyzes each section in the outline and determines what data
    is available to fill it.

    Args:
        state: Current workflow state

    Returns:
        Updates to state with section mappings
    """
    print("🗺️ Mapping content to sections...")

    updates = {
        "current_step": "content_mapper",
        "messages": []
    }

    outline = state.get("contract_outline", [])
    vp_data = state.get("verhandlungsprotokoll_data", {}) or {}
    lv_data = state.get("leistungsverzeichnis_data", {}) or {}

    section_mappings = {}

    for section in outline:
        section_num = section["section_number"]
        section_title = section.get("title_de", "")

        mapping = {
            "section_number": section_num,
            "title": section_title,
            "available_data": [],
            "missing_data": [],
            "completeness": 0.0,
            "priority": section.get("priority", 999)
        }

        # Simple mapping logic based on section content
        title_lower = section_title.lower()

        # Scope/Work sections
        if any(keyword in title_lower for keyword in ["leistung", "scope", "work", "umfang"]):
            if vp_data.get("scope_of_work"):
                mapping["available_data"].append("scope_of_work")
            if lv_data.get("performance_items"):
                mapping["available_data"].append("performance_items")
            if vp_data.get("project_description"):
                mapping["available_data"].append("project_description")

        # Payment/Remuneration sections
        if any(keyword in title_lower for keyword in ["vergütung", "payment", "zahlung", "preis"]):
            if vp_data.get("payment_terms"):
                mapping["available_data"].append("payment_terms")
            if lv_data.get("total_amount"):
                mapping["available_data"].append("total_amount")
            if lv_data.get("subtotal"):
                mapping["available_data"].append("subtotal")

        # Parties sections
        if any(keyword in title_lower for keyword in ["partei", "parties", "vertragspartner"]):
            if vp_data.get("contractor"):
                mapping["available_data"].append("contractor")
            if vp_data.get("subcontractor"):
                mapping["available_data"].append("subcontractor")

        # Dates/Timeline sections
        if any(keyword in title_lower for keyword in ["frist", "termin", "deadline", "date", "zeit"]):
            if vp_data.get("contract_start_date"):
                mapping["available_data"].append("contract_start_date")
            if vp_data.get("contract_end_date"):
                mapping["available_data"].append("contract_end_date")
            if vp_data.get("negotiation_date"):
                mapping["available_data"].append("negotiation_date")

        # Project info sections
        if any(keyword in title_lower for keyword in ["projekt", "project", "bauvorhaben"]):
            if vp_data.get("project_name"):
                mapping["available_data"].append("project_name")
            if vp_data.get("project_location"):
                mapping["available_data"].append("project_location")
            if vp_data.get("project_description"):
                mapping["available_data"].append("project_description")

        # Quality/Standards sections
        if any(keyword in title_lower for keyword in ["qualität", "quality", "standard"]):
            if vp_data.get("quality_standards"):
                mapping["available_data"].append("quality_standards")

        # Warranty sections
        if any(keyword in title_lower for keyword in ["gewährleistung", "warranty", "mängel"]):
            if vp_data.get("warranty_period_months"):
                mapping["available_data"].append("warranty_period_months")

        # Insurance sections
        if any(keyword in title_lower for keyword in ["versicherung", "insurance", "haftung"]):
            if vp_data.get("insurance_requirements"):
                mapping["available_data"].append("insurance_requirements")

        # Calculate completeness (rough estimate)
        if len(mapping["available_data"]) > 0:
            # More data = higher completeness, but cap at 1.0
            mapping["completeness"] = min(1.0, len(mapping["available_data"]) * 0.25)
        else:
            mapping["completeness"] = 0.1  # Some sections can be generated from scratch

        section_mappings[section_num] = mapping

    updates["section_mappings"] = section_mappings

    # Calculate overall data availability
    total_sections = len(section_mappings)
    sections_with_data = sum(1 for m in section_mappings.values() if len(m["available_data"]) > 0)

    updates["messages"].append({
        "role": "system",
        "content": f"✓ Mapped data to {total_sections} sections ({sections_with_data} have extracted data)"
    })

    return updates
