"""Structure analyzer node for building contract outline."""

import json
from typing import Dict, Any
from src.core.llm_clients import get_llm_client
from src.models.contract_drafting_state import ContractDraftingState


def structure_analyzer_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Analyze contract structures and build outline.

    Uses required_sections from contract type + historical structures
    to create a hierarchical contract outline.

    Args:
        state: Current workflow state

    Returns:
        Updates to state with contract outline
    """
    print("📋 Analyzing contract structure...")

    updates = {
        "current_step": "structure_analyzer",
        "messages": []
    }

    contract_type_data = state.get("contract_type_data", {})
    required_sections = contract_type_data.get("required_sections", [])
    retrieved_structures = state.get("contract_structures", [])
    project_description = state.get("project_description", "")

    # Check if we have data
    has_vp = bool(state.get("verhandlungsprotokoll_data"))
    has_lv = bool(state.get("leistungsverzeichnis_data"))

    llm = get_llm_client()

    # Build structure analysis prompt
    prompt = f"""Analyze and create a contract outline for: {contract_type_data.get('name')}

Required Sections (mandatory):
{json.dumps(required_sections, indent=2, ensure_ascii=False)}

{"Historical Structures (examples):" if retrieved_structures else "No historical data available."}
{json.dumps(retrieved_structures[:3], indent=2, ensure_ascii=False) if retrieved_structures else ""}

Project Description:
{project_description}

Available Data:
- Verhandlungsprotokoll: {has_vp}
- Leistungsverzeichnis: {has_lv}

Task:
Create a hierarchical contract outline with:
1. All mandatory sections from required_sections
2. Optional relevant sections based on project (if any)
3. For each section:
   - section_number (e.g., "§1", "§2", ...)
   - title_de (German title)
   - title_en (English title)
   - description (what should be included)
   - mandatory (true for required sections, false otherwise)
   - priority (1=highest, generate first)

Return ONLY a JSON array of sections. No explanations, just the JSON array.

Example format:
[
  {{
    "section_number": "§1",
    "title_de": "Leistungsumfang",
    "title_en": "Scope of Services",
    "description": "Detailed description of work to be performed",
    "mandatory": true,
    "priority": 1
  }},
  ...
]
"""

    try:
        response = llm.invoke([
            {"role": "system", "content": "You are a contract structure expert. Return valid JSON only."},
            {"role": "user", "content": prompt}
        ])

        # Parse JSON response
        outline_text = response.content.strip()

        # Remove markdown code blocks if present
        if "```json" in outline_text:
            outline_text = outline_text.split("```json")[1].split("```")[0]
        elif "```" in outline_text:
            outline_text = outline_text.split("```")[1].split("```")[0]

        contract_outline = json.loads(outline_text.strip())

        # Validate outline
        if not isinstance(contract_outline, list):
            raise ValueError("Outline must be a list")

        updates["contract_outline"] = contract_outline
        updates["messages"].append({
            "role": "system",
            "content": f"✓ Created outline with {len(contract_outline)} sections"
        })

    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️ Failed to parse LLM response, using fallback: {e}")
        # Fallback: use required_sections directly
        updates["contract_outline"] = [
            {
                "section_number": f"§{i+1}",
                "title_de": section,
                "title_en": section,
                "description": f"Standard section for {section}",
                "mandatory": True,
                "priority": i+1
            }
            for i, section in enumerate(required_sections)
        ]
        updates["messages"].append({
            "role": "system",
            "content": f"⚠️ Using fallback outline with {len(required_sections)} sections"
        })

    except Exception as e:
        updates["errors"] = [f"Structure analysis failed: {str(e)}"]
        updates["messages"].append({
            "role": "system",
            "content": f"❌ Structure analysis error: {str(e)}"
        })
        # Minimal fallback
        updates["contract_outline"] = [{
            "section_number": "§1",
            "title_de": "Vertragsgegenstand",
            "title_en": "Subject Matter",
            "description": "Main contract subject",
            "mandatory": True,
            "priority": 1
        }]

    return updates
