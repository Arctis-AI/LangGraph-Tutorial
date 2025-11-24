"""Data merger node for combining data from multiple sources."""

from typing import Dict, Any
from datetime import date
from src.models.state import ContractState
from src.models.contract import ContractData, ContractParty, PaymentTerms


def data_merger_node(state: ContractState) -> Dict[str, Any]:
    """
    Merge data from Verhandlungsprotokoll and Leistungsverzeichnis into unified contract data.
    """
    print("🔀 Merging data from all sources...")

    updates = {
        "current_step": "data_merger",
        "messages": []
    }

    vp_data = state.get("verhandlungsprotokoll_data", {})
    lv_data = state.get("leistungsverzeichnis_data", {})

    try:
        # Prepare contractor and subcontractor - use actual data only
        contractor = vp_data.get("contractor")
        subcontractor = vp_data.get("subcontractor")

        if not contractor or not subcontractor:
            updates["error"] = "Missing contractor or subcontractor data"
            updates["messages"].append({
                "role": "system",
                "content": "❌ Cannot proceed without contractor/subcontractor information"
            })
            return updates

        # Ensure contractor and subcontractor are ContractParty objects
        if isinstance(contractor, dict):
            contractor = ContractParty(**contractor)
        if isinstance(subcontractor, dict):
            subcontractor = ContractParty(**subcontractor)

        # Prepare payment terms - use actual data
        payment_terms = vp_data.get("payment_terms")
        if not payment_terms:
            # Create minimal payment terms if missing
            payment_terms = PaymentTerms(
                payment_schedule=vp_data.get("payment_schedule", "To be defined"),
                payment_deadline_days=30
            )
        if isinstance(payment_terms, dict):
            payment_terms = PaymentTerms(**payment_terms)

        # Merge data into ContractData structure
        merged_data = {
            # Parties
            "contractor": contractor,
            "subcontractor": subcontractor,

            # Project details - use actual extracted data
            "project_name": vp_data.get("project_name", "[Project Name Not Extracted]"),
            "project_location": vp_data.get("project_location", "[Location Not Extracted]"),
            "project_description": vp_data.get("project_description", "[Description Not Extracted]"),
            "project_reference": lv_data.get("project_reference"),

            # Dates
            "contract_date": date.today(),
            "start_date": vp_data.get("contract_start_date", date.today()),
            "end_date": vp_data.get("contract_end_date", date(date.today().year + 1, date.today().month, date.today().day)),

            # Scope and specifications
            "scope_of_work": vp_data.get("scope_of_work", "[Scope Not Extracted]"),
            "performance_items": lv_data.get("performance_items", []),
            "excluded_services": vp_data.get("excluded_services", []),

            # Financial
            "subtotal": lv_data.get("subtotal", 0.0),
            "tax_rate": lv_data.get("tax_rate", 0.19),
            "tax_amount": lv_data.get("tax_amount", 0.0),
            "total_contract_value": lv_data.get("total_amount", 0.0),
            "currency": lv_data.get("currency", "EUR"),

            # Terms and conditions
            "payment_terms": payment_terms,
            "warranty_period_months": vp_data.get("warranty_period_months"),
            "insurance_requirements": vp_data.get("insurance_requirements"),
            "penalties": vp_data.get("penalties"),
            "quality_standards": vp_data.get("quality_standards"),

            # Additional
            "special_agreements": vp_data.get("special_agreements", []),
            "attachments": ["Verhandlungsprotokoll.pdf", "Leistungsverzeichnis.xlsx"],

            # Metadata
            "generated_date": date.today(),
            "version": "1.0"
        }

        # Store the merged data
        updates["merged_data"] = merged_data

        # Generate summary message
        summary_items = [
            f"Project: {merged_data['project_name']}",
            f"Contractor: {merged_data['contractor'].name if hasattr(merged_data['contractor'], 'name') else 'N/A'}",
            f"Subcontractor: {merged_data['subcontractor'].name if hasattr(merged_data['subcontractor'], 'name') else 'N/A'}",
            f"Performance Items: {len(merged_data['performance_items'])}",
            f"Total Value: {merged_data['total_contract_value']:.2f} {merged_data['currency']}",
            f"Duration: {merged_data['start_date']} to {merged_data['end_date']}"
        ]

        updates["messages"].append({
            "role": "system",
            "content": "✓ Successfully merged contract data:\n" + "\n".join(f"  • {item}" for item in summary_items)
        })

    except Exception as e:
        updates["error"] = f"Data merging failed: {str(e)}"
        updates["messages"].append({
            "role": "system",
            "content": f"❌ Data merging error: {str(e)}"
        })
        # Don't use defaults - let the error propagate
        updates["merged_data"] = None

    return updates


