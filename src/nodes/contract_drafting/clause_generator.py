"""Clause generator node for generating contract sections."""

import json
from typing import Dict, Any
from src.core.llm_clients import get_llm_client
from src.models.contract_drafting_state import ContractDraftingState


def clause_generator_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Generate contract sections iteratively.

    Generates each section using:
    - Contract type data and policies
    - Extracted data from documents
    - Historical clause examples
    - Context from previously generated sections

    Args:
        state: Current workflow state

    Returns:
        Updates to state with generated sections and full contract draft
    """
    print("✍️ Generating contract clauses...")

    updates = {
        "current_step": "clause_generator",
        "messages": [],
        "generated_sections": {},
        "contract_draft": ""
    }

    outline = state.get("contract_outline", [])
    section_mappings = state.get("section_mappings", {})
    retrieved_clauses = state.get("retrieved_clauses", [])
    vp_data = state.get("verhandlungsprotokoll_data", {}) or {}
    lv_data = state.get("leistungsverzeichnis_data", {}) or {}
    contract_type_data = state.get("contract_type_data", {})
    project_description = state.get("project_description", "")

    llm = get_llm_client()
    generated_sections = {}

    # Sort by priority
    sorted_outline = sorted(outline, key=lambda x: x.get("priority", 999))

    for idx, section in enumerate(sorted_outline):
        section_num = section["section_number"]
        section_title = section["title_de"]
        section_desc = section.get("description", "")

        print(f"  Generating {section_num} {section_title}...")

        # Get mapping for this section
        mapping = section_mappings.get(section_num, {})

        # Gather relevant data
        section_data = {}
        for data_key in mapping.get("available_data", []):
            if data_key in vp_data:
                section_data[data_key] = vp_data[data_key]
            elif data_key in lv_data:
                section_data[data_key] = lv_data[data_key]

        # Get relevant example clauses
        relevant_clauses = []
        if retrieved_clauses:
            for clause in retrieved_clauses:
                clause_title = clause.get("section_title", "").lower()
                if section_title.lower() in clause_title or clause_title in section_title.lower():
                    relevant_clauses.append(clause)
                if len(relevant_clauses) >= 2:
                    break

        # Build generation prompt
        prompt = f"""Generate contract section: {section_title} ({section_num})

Contract Type: {contract_type_data.get('name')} / {contract_type_data.get('name_de')}
Contract Type Code: {contract_type_data.get('code')}

Project Description:
{project_description[:500] if project_description else "Not provided"}

Section Description:
{section_desc}

Available Data for this Section:
{json.dumps(section_data, indent=2, default=str, ensure_ascii=False) if section_data else "No specific data available"}

{"Reference Clauses (for structure and style):" if relevant_clauses else ""}
{chr(10).join([f"Example {i+1}: {c.get('clause_text', '')[:300]}..." for i, c in enumerate(relevant_clauses)]) if relevant_clauses else ""}

Previously Generated Sections (for context):
{json.dumps({k: v[:150] + "..." for k, v in list(generated_sections.items())[-2:]}, indent=2, ensure_ascii=False) if generated_sections else "This is the first section"}

Instructions:
1. Write in German legal language
2. Use provided data where available (party names, dates, amounts, etc.)
3. Follow structure from examples if provided
4. Be specific and clear
5. If critical information is missing, mark with [PRÜFUNG ERFORDERLICH: reason in German]
6. Ensure consistency with previous sections (party names, terminology)
7. Keep the section focused on {section_title}

Generate ONLY the section text in German. No explanations, no preamble.
"""

        try:
            response = llm.invoke([
                {"role": "system", "content": "You are an expert in drafting German construction contracts. Write precise, legally sound contract text."},
                {"role": "user", "content": prompt}
            ])

            section_text = response.content.strip()
            generated_sections[section_num] = section_text

        except Exception as e:
            print(f"  ⚠️ Failed to generate {section_num}: {e}")
            generated_sections[section_num] = f"[FEHLER BEI DER GENERIERUNG: {str(e)}]\n\n{section_title}\n\n[Dieser Abschnitt muss manuell ergänzt werden]"

    # Compile full contract
    contract_draft = f"""{'='*80}
{contract_type_data.get('name_de', contract_type_data.get('name'))}
{'='*80}

Vertragstyp: {contract_type_data.get('name')}
Code: {contract_type_data.get('code')}

"""

    for section in sorted_outline:
        section_num = section["section_number"]
        section_title = section["title_de"]
        section_text = generated_sections.get(section_num, "[NICHT GENERIERT]")

        contract_draft += f"\n\n{section_num} {section_title}\n"
        contract_draft += "-" * 60 + "\n\n"
        contract_draft += section_text

    # Add signature section
    contract_draft += f"\n\n{'='*80}\n"
    contract_draft += "UNTERSCHRIFTEN / SIGNATURES\n"
    contract_draft += "=" * 80 + "\n\n"

    if vp_data.get("contractor"):
        contractor = vp_data["contractor"]
        contractor_name = contractor.get("name") if hasattr(contractor, "get") else getattr(contractor, "name", "")
        contract_draft += f"Auftraggeber / Client:\n{contractor_name}\n\n"
        contract_draft += "_" * 40 + "\n"
        contract_draft += "Ort, Datum / Place, Date\n\n"
        contract_draft += "_" * 40 + "\n"
        contract_draft += "Unterschrift / Signature\n\n\n"

    if vp_data.get("subcontractor"):
        subcontractor = vp_data["subcontractor"]
        subcontractor_name = subcontractor.get("name") if hasattr(subcontractor, "get") else getattr(subcontractor, "name", "")
        contract_draft += f"Auftragnehmer / Contractor:\n{subcontractor_name}\n\n"
        contract_draft += "_" * 40 + "\n"
        contract_draft += "Ort, Datum / Place, Date\n\n"
        contract_draft += "_" * 40 + "\n"
        contract_draft += "Unterschrift / Signature\n"

    updates["generated_sections"] = generated_sections
    updates["contract_draft"] = contract_draft
    updates["messages"].append({
        "role": "system",
        "content": f"✓ Generated {len(generated_sections)} sections ({len(contract_draft)} characters)"
    })

    return updates
