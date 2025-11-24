"""Data validator node for checking extracted data completeness and consistency."""

from typing import Dict, Any, List
from src.models.state import ContractState


def data_validator_node(state: ContractState) -> Dict[str, Any]:
    """
    Validate extracted data for completeness and consistency.
    """
    print("✅ Validating extracted data...")

    updates = {
        "current_step": "data_validator",
        "validation_errors": [],
        "validation_passed": True,
        "messages": []
    }

    errors = []

    # Check Verhandlungsprotokoll data
    vp_data = state.get("verhandlungsprotokoll_data")
    if vp_data:
        vp_errors = validate_verhandlungsprotokoll(vp_data)
        errors.extend(vp_errors)
        if not vp_errors:
            updates["messages"].append({
                "role": "system",
                "content": "✓ Verhandlungsprotokoll data validation passed"
            })
    else:
        errors.append("Missing Verhandlungsprotokoll data")

    # Check Leistungsverzeichnis data
    lv_data = state.get("leistungsverzeichnis_data")
    if lv_data:
        lv_errors = validate_leistungsverzeichnis(lv_data)
        errors.extend(lv_errors)
        if not lv_errors:
            updates["messages"].append({
                "role": "system",
                "content": "✓ Leistungsverzeichnis data validation passed"
            })
    else:
        errors.append("Missing Leistungsverzeichnis data")

    # Cross-validate if both documents are present
    if vp_data and lv_data:
        cross_errors = cross_validate_documents(vp_data, lv_data)
        errors.extend(cross_errors)
        if not cross_errors:
            updates["messages"].append({
                "role": "system",
                "content": "✓ Cross-document validation passed"
            })

    # Update validation status
    updates["validation_errors"] = errors
    updates["validation_passed"] = len(errors) == 0

    if errors:
        updates["messages"].append({
            "role": "system",
            "content": f"⚠️ Validation found {len(errors)} issue(s):\n" + "\n".join(f"  - {e}" for e in errors[:5])
        })
    else:
        updates["messages"].append({
            "role": "system",
            "content": "✅ All validation checks passed successfully"
        })

    return updates


def validate_verhandlungsprotokoll(data: Dict[str, Any]) -> List[str]:
    """Validate Verhandlungsprotokoll data."""
    errors = []

    # Required fields
    required_fields = [
        "project_name",
        "project_location",
        "contractor",
        "subcontractor",
        "contract_start_date",
        "contract_end_date",
        "scope_of_work",
        "payment_terms"
    ]

    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field in Verhandlungsprotokoll: {field}")

    # Validate dates
    if data.get("contract_start_date") and data.get("contract_end_date"):
        if data["contract_end_date"] <= data["contract_start_date"]:
            errors.append("Contract end date must be after start date")

    # Validate contractor and subcontractor
    if data.get("contractor"):
        contractor = data["contractor"]
        if hasattr(contractor, "name") and not contractor.name:
            errors.append("Contractor name is required")
        if hasattr(contractor, "address") and not contractor.address:
            errors.append("Contractor address is required")

    if data.get("subcontractor"):
        subcontractor = data["subcontractor"]
        if hasattr(subcontractor, "name") and not subcontractor.name:
            errors.append("Subcontractor name is required")
        if hasattr(subcontractor, "address") and not subcontractor.address:
            errors.append("Subcontractor address is required")

    # Validate payment terms
    if data.get("payment_terms"):
        payment_terms = data["payment_terms"]
        if hasattr(payment_terms, "payment_deadline_days"):
            if payment_terms.payment_deadline_days < 0 or payment_terms.payment_deadline_days > 90:
                errors.append("Payment deadline days should be between 0 and 90")

    return errors


def validate_leistungsverzeichnis(data: Dict[str, Any]) -> List[str]:
    """Validate Leistungsverzeichnis data."""
    errors = []

    # Check for performance items
    if not data.get("performance_items") or len(data["performance_items"]) == 0:
        errors.append("No performance items found in Leistungsverzeichnis")

    # Validate each performance item
    for i, item in enumerate(data.get("performance_items", [])):
        if hasattr(item, "quantity") and item.quantity <= 0:
            errors.append(f"Item {i+1}: Invalid quantity ({item.quantity})")
        if hasattr(item, "unit_price") and item.unit_price < 0:
            errors.append(f"Item {i+1}: Invalid unit price ({item.unit_price})")
        if hasattr(item, "total_price"):
            expected_total = round(item.quantity * item.unit_price, 2)
            if abs(item.total_price - expected_total) > 0.01:
                errors.append(f"Item {i+1}: Total price mismatch (expected {expected_total}, got {item.total_price})")

    # Validate totals
    if data.get("subtotal") is not None and data.get("tax_amount") is not None and data.get("total_amount") is not None:
        expected_total = round(data["subtotal"] + data["tax_amount"], 2)
        if abs(data["total_amount"] - expected_total) > 0.01:
            errors.append(f"Total amount mismatch (expected {expected_total}, got {data['total_amount']})")

    # Validate tax rate
    if data.get("tax_rate") is not None:
        if data["tax_rate"] < 0 or data["tax_rate"] > 1:
            errors.append(f"Invalid tax rate: {data['tax_rate']} (should be between 0 and 1)")

    return errors


def cross_validate_documents(vp_data: Dict[str, Any], lv_data: Dict[str, Any]) -> List[str]:
    """Cross-validate data between both documents."""
    errors = []

    # Check if project references match (if available)
    vp_project = vp_data.get("project_name", "").lower()
    lv_project = lv_data.get("project_reference", "").lower()

    if vp_project and lv_project and vp_project not in lv_project and lv_project not in vp_project:
        # Just a warning, not a critical error
        errors.append(f"Project name mismatch warning: '{vp_data.get('project_name')}' vs '{lv_data.get('project_reference')}'")

    return errors