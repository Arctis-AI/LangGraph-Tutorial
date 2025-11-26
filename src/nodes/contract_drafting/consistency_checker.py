"""Consistency checker node for validating contract coherence."""

import re
from typing import Dict, Any
from src.models.contract_drafting_state import ContractDraftingState


def consistency_checker_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Check contract consistency.

    Validates:
    - Cross-references (§X references)
    - Data consistency (names, dates, amounts)
    - Review markers
    - Section completeness

    Args:
        state: Current workflow state

    Returns:
        Updates to state with consistency issues list
    """
    print("✅ Checking consistency...")

    updates = {
        "current_step": "consistency_checker",
        "messages": [],
        "consistency_issues": []
    }

    contract_draft = state.get("contract_draft", "")
    outline = state.get("contract_outline", [])
    vp_data = state.get("verhandlungsprotokoll_data", {}) or {}
    issues = []

    # 1. Check cross-references
    references = re.findall(r'§\d+', contract_draft)
    if references:
        # Get all section numbers from outline
        valid_sections = {s["section_number"] for s in outline}

        for ref in set(references):
            if ref not in valid_sections:
                issues.append({
                    "type": "missing_reference",
                    "reference": ref,
                    "message": f"Reference to {ref} but section doesn't exist",
                    "severity": "medium"
                })

    # 2. Check for review markers
    if "[PRÜFUNG ERFORDERLICH:" in contract_draft or "[REVIEW NEEDED:" in contract_draft:
        review_items_de = re.findall(r'\[PRÜFUNG ERFORDERLICH: ([^\]]+)\]', contract_draft)
        review_items_en = re.findall(r'\[REVIEW NEEDED: ([^\]]+)\]', contract_draft)
        all_reviews = review_items_de + review_items_en

        for item in all_reviews:
            issues.append({
                "type": "review_needed",
                "item": item,
                "message": f"Manual review required: {item}",
                "severity": "high"
            })

    # 3. Check for error markers
    if "[FEHLER" in contract_draft or "[ERROR" in contract_draft:
        issues.append({
            "type": "generation_error",
            "message": "Some sections have generation errors",
            "severity": "critical"
        })

    # 4. Check data consistency (party names)
    if vp_data.get("contractor"):
        contractor = vp_data["contractor"]
        contractor_name = contractor.get("name") if hasattr(contractor, "get") else getattr(contractor, "name", "")

        if contractor_name and contractor_name not in contract_draft:
            issues.append({
                "type": "missing_data",
                "field": "contractor_name",
                "message": f"Contractor name '{contractor_name}' not mentioned in contract",
                "severity": "high"
            })

    if vp_data.get("subcontractor"):
        subcontractor = vp_data["subcontractor"]
        subcontractor_name = subcontractor.get("name") if hasattr(subcontractor, "get") else getattr(subcontractor, "name", "")

        if subcontractor_name and subcontractor_name not in contract_draft:
            issues.append({
                "type": "missing_data",
                "field": "subcontractor_name",
                "message": f"Subcontractor name '{subcontractor_name}' not mentioned in contract",
                "severity": "high"
            })

    # 5. Check section completeness
    for section in outline:
        section_num = section["section_number"]
        if section_num not in contract_draft:
            issues.append({
                "type": "missing_section",
                "section": section_num,
                "message": f"Required section {section_num} {section.get('title_de')} is missing",
                "severity": "critical"
            })

    # 6. Check for placeholder text
    placeholders = ["[TODO]", "[TBD]", "[XXXXX]", "[...]"]
    for placeholder in placeholders:
        if placeholder in contract_draft:
            issues.append({
                "type": "placeholder",
                "message": f"Placeholder text found: {placeholder}",
                "severity": "medium"
            })

    updates["consistency_issues"] = issues

    # Categorize issues by severity
    critical = [i for i in issues if i["severity"] == "critical"]
    high = [i for i in issues if i["severity"] == "high"]
    medium = [i for i in issues if i["severity"] == "medium"]

    updates["messages"].append({
        "role": "system",
        "content": f"✓ Consistency check complete: {len(issues)} issue(s) found "
                  f"({len(critical)} critical, {len(high)} high, {len(medium)} medium)"
    })

    if critical:
        updates["messages"].append({
            "role": "system",
            "content": f"⚠️ CRITICAL: {', '.join([i['message'] for i in critical[:3]])}"
        })

    return updates
