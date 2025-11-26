"""Example script to run the contract drafting workflow."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.contract_drafting_graph import create_contract_drafting_graph
from datetime import datetime


def main():
    """
    Run the contract drafting workflow with example data.
    """
    print("="*80)
    print("CONTRACT DRAFTING WORKFLOW - EXAMPLE RUN")
    print("="*80)
    print()

    # Initialize the graph
    graph = create_contract_drafting_graph()

    # Example 1: Site Supervision Subcontract with documents
    print("\n🔹 Example 1: Site Supervision Subcontract\n")

    initial_state = {
        # Contract type selection
        "contract_type_id": "00827bca-eccf-4e5a-87bb-dcd438c4ff29",  # Site Supervision

        # Project description
        "project_description": """
        Bauüberwachung für ein Bürogebäudeprojekt in Berlin.
        Das Projekt umfasst den Neubau eines 5-stöckigen Bürogebäudes mit ca. 3.000 qm Nutzfläche.
        Die Bauüberwachung soll die Qualitätskontrolle, Sicherheitsmanagement und
        Fortschrittsberichterstattung für die gesamte Bauphase von 18 Monaten umfassen.
        """,

        # Documents (if available)
        "uploaded_documents": [
            # {
            #     "type": "verhandlungsprotokoll",
            #     "path": "data/uploads/verhandlungsprotokoll.pdf"
            # },
            # {
            #     "type": "leistungsverzeichnis",
            #     "path": "data/uploads/leistungsverzeichnis.xlsx"
            # }
        ],

        # Initialize required fields
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

    try:
        # Run the workflow
        print("🚀 Starting workflow...\n")

        result = graph.invoke(
            initial_state,
            config={"configurable": {"thread_id": "example-1"}}
        )

        # Print results
        print("\n" + "="*80)
        print("WORKFLOW COMPLETED")
        print("="*80)
        print()

        print(f"📊 Quality Score: {result.get('quality_score', 0):.1f}/100")
        print(f"📋 Sections Generated: {len(result.get('generated_sections', {}))}")
        print(f"⚠️  Consistency Issues: {len(result.get('consistency_issues', []))}")
        print()

        # Print output files
        print("📁 Output Files:")
        for file_type, path in result.get('output_files', {}).items():
            print(f"   {file_type.upper()}: {path}")
        print()

        # Print messages
        print("📝 Workflow Messages:")
        for msg in result.get('messages', [])[-10:]:  # Last 10 messages
            if isinstance(msg, dict):
                content = msg.get('content', str(msg))
            else:
                content = str(msg)
            print(f"   {content}")
        print()

        # Print contract preview
        contract_draft = result.get('contract_draft', '')
        if contract_draft:
            print("📄 Contract Preview (first 500 chars):")
            print("-" * 80)
            print(contract_draft[:500])
            print("...")
            print("-" * 80)
        print()

        print("✅ Workflow completed successfully!")

    except Exception as e:
        print(f"\n❌ Error running workflow: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
