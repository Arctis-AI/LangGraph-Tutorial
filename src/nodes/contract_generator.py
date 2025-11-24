"""Contract generator node for creating contract draft from merged data."""

import os
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
from src.models.state import ContractState


def contract_generator_node(state: ContractState) -> Dict[str, Any]:
    """
    Generate contract draft using Jinja2 template and merged data.
    """
    print("📝 Generating contract draft...")

    updates = {
        "current_step": "contract_generator",
        "messages": []
    }

    merged_data = state.get("merged_data")
    if not merged_data:
        updates["error"] = "No merged data available for contract generation"
        updates["messages"].append({
            "role": "system",
            "content": "❌ Cannot generate contract: No merged data available"
        })
        return updates

    try:
        # Setup Jinja2 environment
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
        env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Load template
        template = env.get_template("contract_template.jinja2")

        # Render contract
        contract_draft = template.render(**merged_data)

        updates["contract_draft"] = contract_draft
        updates["messages"].append({
            "role": "system",
            "content": f"✓ Generated contract draft ({len(contract_draft)} characters)"
        })

        # Generate summary
        summary_lines = contract_draft.split('\n')[:50]  # First 50 lines for preview
        preview = '\n'.join(summary_lines[:10]) + "\n...\n[Contract continues...]"

        updates["messages"].append({
            "role": "system",
            "content": f"📄 Contract Preview:\n{preview}"
        })

    except Exception as e:
        updates["error"] = f"Contract generation failed: {str(e)}"
        updates["messages"].append({
            "role": "system",
            "content": f"❌ Contract generation error: {str(e)}"
        })
        # Create a basic fallback contract
        updates["contract_draft"] = create_fallback_contract(merged_data)

    return updates


def create_fallback_contract(data: Dict[str, Any]) -> str:
    """Create a basic fallback contract when template rendering fails."""
    contractor_name = "Unknown Contractor"
    subcontractor_name = "Unknown Subcontractor"

    if data.get("contractor") and hasattr(data["contractor"], "name"):
        contractor_name = data["contractor"].name
    if data.get("subcontractor") and hasattr(data["subcontractor"], "name"):
        subcontractor_name = data["subcontractor"].name

    return f"""
NACHUNTERNEHMERVERTRAG / SUBCONTRACTOR AGREEMENT

Between:
{contractor_name}
- hereinafter "Contractor" -

and:
{subcontractor_name}
- hereinafter "Subcontractor" -

Project: {data.get('project_name', 'Unknown Project')}
Location: {data.get('project_location', 'Unknown Location')}

Total Contract Value: {data.get('total_contract_value', 0):.2f} {data.get('currency', 'EUR')}

Start Date: {data.get('start_date', 'TBD')}
End Date: {data.get('end_date', 'TBD')}

[FALLBACK CONTRACT - TEMPLATE RENDERING FAILED]

This is a minimal contract draft. Please review and complete all necessary sections.
"""