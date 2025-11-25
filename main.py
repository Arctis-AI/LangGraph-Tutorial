"""
Contract Generation System - Main Entry Point

This system generates subcontractor contracts from:
1. Verhandlungsprotokoll (negotiation protocol) - PDF/Text
2. Leistungsverzeichnis (bill of quantities) - Excel
"""

from dotenv import load_dotenv
import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.contract_graph import create_contract_graph_with_routing

# Load environment variables
load_dotenv()


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 80)
    print("  NACHUNTERNEHMERVERTRAG GENERATOR")
    print("  Subcontractor Contract Generation System")
    print("=" * 80)
    print()


def print_step(step: str, message: str):
    """Print a step in the process."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {step}: {message}")


def run_contract_generation():
    """Run the contract generation workflow."""
    print_banner()

    print("📋 Starting contract generation process...")
    print("📁 Looking for documents in 'resource' folder...")
    print()

    # Initialize the graph with conditional routing
    print_step("INIT", "Building workflow graph...")
    graph = create_contract_graph_with_routing()

    # Initialize state
    initial_state = {
        "messages": [],
        "uploaded_files": {},
        "validation_errors": [],
        "validation_passed": False,
        "quality_passed": False,
        "retry_count": 0,
        "processing_status": "starting",
        "current_step": "init"
    }

    # Run the workflow
    print_step("START", "Executing workflow...")
    print("-" * 80)

    try:
        # Execute the graph
        final_state = graph.invoke(
            initial_state,
            {"configurable": {"thread_id": "contract_gen_001"}}
        )

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

        # Display validation results
        if final_state.get("validation_errors"):
            print(f"\n⚠️ Validation Issues: {len(final_state['validation_errors'])}")
            for error in final_state["validation_errors"][:5]:
                print(f"  - {error}")

        # Display quality report
        if final_state.get("quality_report"):
            report = final_state["quality_report"]
            print(f"\n📈 Quality Report:")
            print(f"  Score: {report.get('score', 0):.1f}%")
            print(f"  Checks Passed: {report.get('passed', 0)}/{report.get('total', 0)}")

        # Display output information
        if final_state.get("output_path"):
            print(f"\n✅ Contract generated successfully!")
            print(f"📁 Output file: {final_state['output_path']}")
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
        description="Generate subcontractor contracts from documents"
    )
    parser.add_argument(
        "--pdf",
        help="Path to Verhandlungsprotokoll (PDF/TXT)",
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

    # If custom paths provided, update the resource files
    if args.pdf or args.excel:
        print("⚠️ Custom file paths not yet implemented. Using default resources folder.")

    # Run the generation
    run_contract_generation()


if __name__ == "__main__":
    main()
