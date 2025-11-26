"""Prompts for document extraction tasks."""


def DOCUMENT_EXTRACTION_PROMPT(full_text: str) -> str:
    """
    Generate the extraction prompt for Verhandlungsprotokoll documents.

    Args:
        full_text: The text to analyze (limited to first 8000 characters)

    Returns:
        The formatted extraction prompt
    """
    return f"""
You are a contract data extraction specialist. Extract structured information from this German negotiation protocol (Verhandlungsprotokoll).

Text to analyze:
{full_text[:8000]}

IMPORTANT: Extract ACTUAL information from the text above. Do not use placeholder or example data.

Extract the following information and return it as a valid JSON object:
{{
    "project_name": "Project name",
    "project_location": "Project location/address",
    "project_description": "Detailed project description",
    "contractor": {{
        "name": "Contractor company name",
        "address": "Contractor address",
        "registration_number": "Registration number if available",
        "tax_id": "Tax ID if available",
        "contact_person": "Contact person if mentioned",
        "email": "Email if mentioned",
        "phone": "Phone if mentioned"
    }},
    "subcontractor": {{
        "name": "Subcontractor company name",
        "address": "Subcontractor address",
        "registration_number": "Registration number if available",
        "tax_id": "Tax ID if available",
        "contact_person": "Contact person if mentioned",
        "email": "Email if mentioned",
        "phone": "Phone if mentioned"
    }},
    "negotiation_date": "YYYY-MM-DD format or null",
    "contract_start_date": "YYYY-MM-DD format",
    "contract_end_date": "YYYY-MM-DD format",
    "scope_of_work": "Detailed scope of work description",
    "payment_terms": {{
        "payment_schedule": "Payment schedule description",
        "advance_payment": "Advance payment percentage or null",
        "retention": "Retention percentage or null",
        "payment_deadline_days": "Days for payment (default 30)",
        "final_payment_conditions": "Conditions for final payment or null"
    }},
    "warranty_period_months": "Warranty period in months or null",
    "insurance_requirements": "Required insurances or null",
    "special_agreements": ["List of special agreements"],
    "excluded_services": ["List of explicitly excluded services"],
    "penalties": "Penalty clauses or null",
    "quality_standards": "Required quality standards or null"
}}

If information is not found in the text, use reasonable defaults or null values.
Ensure all dates are in YYYY-MM-DD format.
Return ONLY the JSON object, no additional text.
"""


def FIELD_EXTRACTION_PROMPT_TEMPLATE(field_name: str, prompt: str, text: str) -> str:
    """
    Generate a targeted field extraction prompt.

    Args:
        field_name: The name of the field being extracted
        prompt: The specific instruction for extracting this field
        text: The text to extract from (limited to first 2000 characters)

    Returns:
        The formatted prompt
    """
    return f"{prompt}\n\nText:\n{text[:2000]}"