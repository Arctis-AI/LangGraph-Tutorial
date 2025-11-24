"""Upload handler node for processing input files."""

import os
from typing import Dict, Any
from src.models.state import ContractState


def upload_handler_node(state: ContractState) -> Dict[str, Any]:
    """
    Handle file uploads and validate their existence.
    For this POC, we'll use static files from the resources folder.
    """
    print("📁 Processing uploaded files...")

    # Define paths to resource files
    resources_dir = "resources"
    # Check for PDF or text file
    pdf_file = os.path.join(resources_dir, "verhandlungsprotokoll.pdf")
    if not os.path.exists(pdf_file):
        # Fall back to text file
        pdf_file = os.path.join(resources_dir, "verhandlungsprotokoll.txt")
    excel_file = os.path.join(resources_dir, "leistungsverzeichnis.xlsx")

    updates = {
        "current_step": "upload_handler",
        "processing_status": "files_uploaded",
        "uploaded_files": {},
        "messages": [{"role": "system", "content": "Starting contract generation process..."}]
    }

    # Check for PDF file
    if os.path.exists(pdf_file):
        updates["pdf_path"] = pdf_file
        updates["uploaded_files"]["pdf"] = pdf_file
        updates["messages"].append({
            "role": "system",
            "content": f"✓ Found Verhandlungsprotokoll: {pdf_file}"
        })
    else:
        updates["messages"].append({
            "role": "system",
            "content": f"⚠️ Verhandlungsprotokoll not found at: {pdf_file}"
        })

    # Check for Excel file
    if os.path.exists(excel_file):
        updates["excel_path"] = excel_file
        updates["uploaded_files"]["excel"] = excel_file
        updates["messages"].append({
            "role": "system",
            "content": f"✓ Found Leistungsverzeichnis: {excel_file}"
        })
    else:
        updates["messages"].append({
            "role": "system",
            "content": f"⚠️ Leistungsverzeichnis not found at: {excel_file}"
        })

    # Validate that we have at least one file
    if not updates["uploaded_files"]:
        updates["error"] = "No input files found. Please add files to the resources folder."
        updates["processing_status"] = "error"
    else:
        updates["messages"].append({
            "role": "system",
            "content": f"Successfully loaded {len(updates['uploaded_files'])} file(s)"
        })

    return updates