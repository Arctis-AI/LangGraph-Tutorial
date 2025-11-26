"""User input handler node for contract drafting."""

import json
import os
from typing import Dict, Any
from src.models.contract_drafting_state import ContractDraftingState


def user_input_handler_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Handle user inputs: contract type selection, description, documents.

    Args:
        state: Current workflow state

    Returns:
        Updates to state with validated inputs and contract type data
    """
    print("📝 Processing user inputs...")

    updates = {
        "current_step": "user_input_handler",
        "messages": []
    }

    # Load contract type data from JSON
    contract_type_id = state.get("contract_type_id")
    if not contract_type_id:
        updates["errors"] = ["No contract type ID provided"]
        updates["messages"].append({
            "role": "system",
            "content": "❌ No contract type selected"
        })
        return updates

    contract_types = load_contract_types()
    contract_type_data = next(
        (ct for ct in contract_types if ct["id"] == contract_type_id),
        None
    )

    if not contract_type_data:
        updates["errors"] = [f"Contract type {contract_type_id} not found"]
        updates["messages"].append({
            "role": "system",
            "content": f"❌ Contract type {contract_type_id} not found"
        })
        return updates

    # Store contract type data
    updates["contract_type_data"] = contract_type_data
    updates["contract_type_code"] = contract_type_data["code"]

    updates["messages"].append({
        "role": "system",
        "content": f"✓ Contract type selected: {contract_type_data.get('name')} ({contract_type_data.get('name_de')})"
    })

    # Validate project description
    project_description = state.get("project_description", "")
    if not project_description or len(project_description.strip()) < 10:
        updates["messages"].append({
            "role": "system",
            "content": "⚠️ Project description is very short - consider adding more details"
        })

    # Validate documents
    uploaded_docs = state.get("uploaded_documents", [])
    if not uploaded_docs:
        updates["messages"].append({
            "role": "system",
            "content": "⚠️ No documents uploaded - contract will be generated from contract type template only"
        })
    else:
        # Map documents to pdf_path and excel_path for existing extractors
        for doc in uploaded_docs:
            doc_type = doc.get("type", "").lower()
            doc_path = doc.get("path", "")

            if doc_type == "verhandlungsprotokoll" or doc_path.endswith(('.pdf', '.docx', '.txt')):
                updates["pdf_path"] = doc_path
            elif doc_type == "leistungsverzeichnis" or doc_path.endswith(('.xlsx', '.xls', '.csv')):
                updates["excel_path"] = doc_path

        updates["messages"].append({
            "role": "system",
            "content": f"✓ {len(uploaded_docs)} document(s) uploaded"
        })

    # Log required sections
    required_sections = contract_type_data.get("required_sections", [])
    updates["messages"].append({
        "role": "system",
        "content": f"📋 Contract type requires {len(required_sections)} mandatory sections"
    })

    updates["processing_status"] = "inputs_validated"

    return updates


def load_contract_types():
    """Load contract types from JSON file."""
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    json_path = os.path.join(project_root, "knowledge_base", "contract_types", "contract_types_rows.json")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Contract types file not found at {json_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"⚠️ Error parsing contract types JSON: {e}")
        return []
