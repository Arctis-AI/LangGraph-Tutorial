"""Quality reviewer node for assessing contract quality."""

from typing import Dict, Any
from src.models.contract_drafting_state import ContractDraftingState


def quality_reviewer_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Review contract quality.

    Assesses:
    - Completeness (all sections present)
    - Data usage (how much extracted data used)
    - Consistency (issues found)
    - Length and detail

    Args:
        state: Current workflow state

    Returns:
        Updates to state with quality report and score
    """
    print("⭐ Reviewing quality...")

    updates = {
        "current_step": "quality_reviewer",
        "messages": []
    }

    contract_draft = state.get("contract_draft", "")
    consistency_issues = state.get("consistency_issues", [])
    outline = state.get("contract_outline", [])
    generated_sections = state.get("generated_sections", {})
    section_mappings = state.get("section_mappings", {})

    # Start with perfect score
    quality_score = 100.0

    # 1. Penalize for consistency issues
    for issue in consistency_issues:
        if issue["severity"] == "critical":
            quality_score -= 15
        elif issue["severity"] == "high":
            quality_score -= 10
        elif issue["severity"] == "medium":
            quality_score -= 5

    # 2. Penalize for short contract
    if len(contract_draft) < 500:
        quality_score -= 30
    elif len(contract_draft) < 1000:
        quality_score -= 20
    elif len(contract_draft) < 2000:
        quality_score -= 10

    # 3. Penalize for missing sections
    missing_sections = len(outline) - len(generated_sections)
    quality_score -= missing_sections * 15

    # 4. Reward for data usage
    sections_with_data = sum(
        1 for mapping in section_mappings.values()
        if len(mapping.get("available_data", [])) > 0
    )
    data_usage_ratio = sections_with_data / max(1, len(section_mappings))
    quality_bonus = data_usage_ratio * 10
    quality_score += quality_bonus

    # 5. Ensure score is in range
    quality_score = max(0, min(100, quality_score))

    # Calculate section scores
    section_scores = {}
    for section in outline:
        section_num = section["section_number"]
        section_text = generated_sections.get(section_num, "")

        score = 100
        if not section_text:
            score = 0
        elif "[FEHLER" in section_text or "[ERROR" in section_text:
            score = 20
        elif "[PRÜFUNG" in section_text or "[REVIEW" in section_text:
            score = 60
        elif len(section_text) < 100:
            score = 50

        section_scores[section_num] = score

    # Determine quality level
    if quality_score >= 85:
        quality_level = "Excellent"
    elif quality_score >= 70:
        quality_level = "Good"
    elif quality_score >= 50:
        quality_level = "Fair"
    else:
        quality_level = "Poor"

    # Build quality report
    quality_report = {
        "score": round(quality_score, 1),
        "level": quality_level,
        "issues_count": len(consistency_issues),
        "critical_issues": [i for i in consistency_issues if i["severity"] == "critical"],
        "sections_generated": len(generated_sections),
        "sections_required": len(outline),
        "contract_length": len(contract_draft),
        "section_scores": section_scores,
        "data_usage_ratio": round(data_usage_ratio, 2)
    }

    updates["quality_report"] = quality_report
    updates["quality_score"] = quality_score
    updates["quality_passed"] = quality_score >= 50  # Minimum threshold

    # Build message
    message = f"✓ Quality assessment complete: {quality_score:.1f}/100 ({quality_level})\n"
    message += f"  - {len(generated_sections)}/{len(outline)} sections generated\n"
    message += f"  - {len(consistency_issues)} consistency issues\n"
    message += f"  - {round(data_usage_ratio * 100)}% sections use extracted data"

    updates["messages"].append({
        "role": "system",
        "content": message
    })

    if quality_score < 70:
        updates["messages"].append({
            "role": "system",
            "content": "⚠️ Quality score below 70 - manual review strongly recommended"
        })

    return updates
