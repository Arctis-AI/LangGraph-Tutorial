"""
Contract Generation System - Main Entry Point

This system generates construction contracts from:
1. Contract type selection (94 types available)
2. Project description
3. Supporting documents (optional):
   - Verhandlungsprotokoll (negotiation protocol) - PDF/DOCX/TXT
   - Leistungsverzeichnis (bill of quantities) - Excel
"""

from dotenv import load_dotenv
import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.contract_drafting_graph import create_contract_drafting_graph

# Load environment variables
load_dotenv()


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 80)
    print("  CONSTRUCTION CONTRACT DRAFTING SYSTEM")
    print("  AI-Powered General Contract Generation")
    print("=" * 80)
    print()


def print_step(step: str, message: str):
    """Print a step in the process."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {step}: {message}")


def run_contract_generation(contract_type_id=None, project_description=None, pdf_path=None, excel_path=None):
    """Run the contract generation workflow."""
    print_banner()

    print("📋 Starting contract generation process...")
    print()

    # Initialize the graph
    print_step("INIT", "Building workflow graph...")
    graph = create_contract_drafting_graph()

    # Use default contract type if not provided (Site Supervision)
    if not contract_type_id:
        contract_type_id = "00827bca-eccf-4e5a-87bb-dcd438c4ff29"  # Site Supervision
        print_step("DEFAULT", "Using default contract type: Site Supervision Subcontract")

    # Use default description if not provided
    if not project_description:
        project_description = """
        Bauüberwachung für ein Bauprojekt.
        Die Überwachung umfasst Qualitätskontrolle, Sicherheitsmanagement und Fortschrittsberichterstattung.
        """
        print_step("DEFAULT", "Using default project description")

    # Check for documents in resource folder if not provided
    uploaded_documents = []

    # Look for PDF/DOCX (Verhandlungsprotokoll)
    if pdf_path:
        if os.path.exists(pdf_path):
            uploaded_documents.append({"type": "verhandlungsprotokoll", "path": pdf_path})
            print_step("FOUND", f"Verhandlungsprotokoll: {pdf_path}")
    else:
        # Search for VP documents in resource folder
        import glob
        vp_patterns = [
            "resource/*Verhandlungsprotokoll*.pdf",
            "resource/*Verhandlungsprotokoll*.docx",
            "resource/*verhandlungsprotokoll*.pdf",
            "resource/*verhandlungsprotokoll*.docx",
            "resource/*.pdf",
            "resource/*.docx"
        ]
        for pattern in vp_patterns:
            files = glob.glob(pattern)
            if files:
                doc_path = files[0]  # Take first match
                uploaded_documents.append({"type": "verhandlungsprotokoll", "path": doc_path})
                print_step("FOUND", f"Verhandlungsprotokoll: {doc_path}")
                break

    # Look for Excel (Leistungsverzeichnis)
    if excel_path:
        if os.path.exists(excel_path):
            uploaded_documents.append({"type": "leistungsverzeichnis", "path": excel_path})
            print_step("FOUND", f"Leistungsverzeichnis: {excel_path}")
    else:
        # Search for LV documents in resource folder
        lv_patterns = [
            "resource/*Leistungsverzeichnis*.xlsx",
            "resource/*Leistungsverzeichnis*.xls",
            "resource/*leistungsverzeichnis*.xlsx",
            "resource/*leistungsverzeichnis*.xls",
            "resource/*.xlsx",
            "resource/*.xls"
        ]
        for pattern in lv_patterns:
            files = glob.glob(pattern)
            if files:
                doc_path = files[0]  # Take first match
                uploaded_documents.append({"type": "leistungsverzeichnis", "path": doc_path})
                print_step("FOUND", f"Leistungsverzeichnis: {doc_path}")
                break

    if not uploaded_documents:
        print_step("INFO", "No documents found - will generate from contract type template")

    # Initialize state
    initial_state = {
        "contract_type_id": contract_type_id,
        "project_description": project_description,
        "uploaded_documents": uploaded_documents,
        "messages": [],
        "errors": [],
        "retrieved_contracts": [],
        "retrieved_clauses": [],
        "contract_structures": [],
        "consistency_issues": [],
        "output_files": {},
        "generated_sections": {},
        "section_mappings": {},
        "contract_outline": [],
        "quality_report": {},
        "quality_score": 0.0,
        "quality_passed": False,
        "current_step": "",
        "processing_status": "initialized",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    # Run the workflow
    print_step("START", "Executing workflow...")
    print("-" * 80)

    try:
        # Execute the graph with metadata for LangSmith
        config = {
            "configurable": {"thread_id": "contract_gen_001"},
            "run_name": "Contract Drafting - General",
            "tags": ["contract_drafting", "general", f"type_{contract_type_id[:8]}"]
        }

        final_state = graph.invoke(initial_state, config)

        # Print results
        print("\n" + "=" * 80)
        print("  WORKFLOW COMPLETED")
        print("=" * 80)

        # Display messages from the workflow
        if final_state.get("messages"):
            print("\n📊 Process Log:")
            for msg in final_state["messages"]:
                if isinstance(msg, dict) and msg.get("content"):
                    print(f"  {msg['content']}")
                else:
                    print(f"  {msg}")

        # Display consistency issues
        consistency_issues = final_state.get("consistency_issues", [])
        if consistency_issues:
            print(f"\n⚠️ Consistency Issues: {len(consistency_issues)}")
            for issue in consistency_issues[:5]:
                severity = issue.get("severity", "unknown")
                message = issue.get("message", str(issue))
                print(f"  [{severity.upper()}] {message}")

        # Display quality report
        quality_report = final_state.get("quality_report", {})
        if quality_report:
            print(f"\n📈 Quality Report:")
            print(f"  Score: {quality_report.get('score', 0):.1f}/100")
            print(f"  Level: {quality_report.get('level', 'N/A')}")
            print(f"  Sections: {quality_report.get('sections_generated', 0)}/{quality_report.get('sections_required', 0)}")
            print(f"  Contract Length: {quality_report.get('contract_length', 0)} chars")

        # Display output information
        output_files = final_state.get("output_files", {})
        if output_files:
            print(f"\n✅ Contract generated successfully!")
            print(f"📁 Output files:")
            for file_type, path in output_files.items():
                print(f"  - {file_type.upper()}: {path}")
        else:
            print("\n❌ Contract generation did not complete successfully.")

        # Show a preview if available
        if final_state.get("contract_draft"):
            print("\n📄 Contract Preview (first 500 characters):")
            print("-" * 40)
            preview = final_state["contract_draft"][:500]
            print(preview)
            if len(final_state["contract_draft"]) > 500:
                print("\n[... document continues ...]")

    except Exception as e:
        print(f"\n❌ Error during workflow execution: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 80)
    print("  Process complete. Check 'data/output' folder for generated contracts.")
    print("=" * 80 + "\n")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate construction contracts from project description and documents"
    )
    parser.add_argument(
        "--contract-type",
        help="Contract type ID (default: Site Supervision)",
        default=None
    )
    parser.add_argument(
        "--description",
        help="Project description",
        default=None
    )
    parser.add_argument(
        "--pdf",
        help="Path to Verhandlungsprotokoll (PDF/DOCX/TXT)",
        default=None
    )
    parser.add_argument(
        "--excel",
        help="Path to Leistungsverzeichnis (XLSX)",
        default=None
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed processing information"
    )

    args = parser.parse_args()

    # Run the generation
    run_contract_generation(
        contract_type_id=args.contract_type,
        project_description=args.description,
        pdf_path=args.pdf,
        excel_path=args.excel
    )


if __name__ == "__main__":
    main()
