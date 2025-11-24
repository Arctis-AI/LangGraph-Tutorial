"""PDF extractor node for processing Verhandlungsprotokoll."""

import pdfplumber
from typing import Dict, Any
from datetime import date, datetime
from langchain.chat_models import init_chat_model
from src.models.state import ContractState
from src.models.contract import VerhandlungsprotokollData, ContractParty, PaymentTerms
import json


def pdf_extractor_node(state: ContractState) -> Dict[str, Any]:
    """
    Extract data from Verhandlungsprotokoll PDF using pdfplumber and LLM.
    """
    print("📄 Extracting data from Verhandlungsprotokoll...")

    updates = {
        "current_step": "pdf_extractor",
        "messages": []
    }

    pdf_path = state.get("pdf_path")
    if not pdf_path:
        updates["messages"].append({
            "role": "system",
            "content": "⚠️ No PDF file available, skipping PDF extraction"
        })
        return updates

    try:
        # Extract text from PDF or text file
        full_text = ""
        if pdf_path.endswith('.txt'):
            # Read text file directly
            with open(pdf_path, 'r', encoding='utf-8') as f:
                full_text = f.read()
        else:
            # Extract from PDF
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"

        updates["verhandlungsprotokoll_raw"] = full_text
        updates["messages"].append({
            "role": "system",
            "content": f"✓ Extracted {len(full_text)} characters from PDF"
        })

        # Use LLM to structure the extracted data
        llm = init_chat_model("anthropic:claude-sonnet-4-20250514")

        extraction_prompt = f"""
        You are a contract data extraction specialist. Extract structured information from this German negotiation protocol (Verhandlungsprotokoll).

        Text to analyze:
        {full_text[:8000]}  # Limit to avoid token limits

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

        response = llm.invoke([
            {"role": "system", "content": "You are a precise data extraction assistant."},
            {"role": "user", "content": extraction_prompt}
        ])

        # Parse the LLM response as JSON
        try:
            extracted_data = json.loads(response.content)

            # Convert date strings to date objects where needed
            if extracted_data.get("negotiation_date"):
                extracted_data["negotiation_date"] = datetime.strptime(
                    extracted_data["negotiation_date"], "%Y-%m-%d"
                ).date()
            if extracted_data.get("contract_start_date"):
                extracted_data["contract_start_date"] = datetime.strptime(
                    extracted_data["contract_start_date"], "%Y-%m-%d"
                ).date()
            if extracted_data.get("contract_end_date"):
                extracted_data["contract_end_date"] = datetime.strptime(
                    extracted_data["contract_end_date"], "%Y-%m-%d"
                ).date()

            # Create structured objects
            extracted_data["contractor"] = ContractParty(**extracted_data["contractor"])
            extracted_data["subcontractor"] = ContractParty(**extracted_data["subcontractor"])
            extracted_data["payment_terms"] = PaymentTerms(**extracted_data["payment_terms"])

            updates["verhandlungsprotokoll_data"] = extracted_data
            updates["messages"].append({
                "role": "system",
                "content": "✓ Successfully structured Verhandlungsprotokoll data"
            })

        except json.JSONDecodeError as e:
            # If JSON parsing fails, create default data
            updates["verhandlungsprotokoll_data"] = create_default_verhandlungsprotokoll_data()
            updates["messages"].append({
                "role": "system",
                "content": f"⚠️ Could not parse LLM response, using defaults: {str(e)}"
            })

    except Exception as e:
        updates["error"] = f"PDF extraction failed: {str(e)}"
        updates["messages"].append({
            "role": "system",
            "content": f"❌ PDF extraction error: {str(e)}"
        })
        # Create default data on error
        updates["verhandlungsprotokoll_data"] = create_default_verhandlungsprotokoll_data()

    return updates


def create_default_verhandlungsprotokoll_data() -> Dict[str, Any]:
    """Create default Verhandlungsprotokoll data structure."""
    return {
        "project_name": "Construction Project",
        "project_location": "Berlin, Germany",
        "project_description": "General construction work",
        "contractor": ContractParty(
            name="Main Contractor GmbH",
            address="Sample Street 1, 10115 Berlin",
            registration_number="HRB 12345",
            contact_person="John Doe",
            email="info@contractor.de",
            phone="+49 30 123456"
        ),
        "subcontractor": ContractParty(
            name="Subcontractor AG",
            address="Work Street 2, 10117 Berlin",
            registration_number="HRB 67890",
            contact_person="Jane Smith",
            email="info@subcontractor.de",
            phone="+49 30 789012"
        ),
        "negotiation_date": date.today(),
        "contract_start_date": date.today(),
        "contract_end_date": date(date.today().year + 1, date.today().month, date.today().day),
        "scope_of_work": "Complete construction work as per specifications",
        "payment_terms": PaymentTerms(
            payment_schedule="Monthly progress payments",
            advance_payment=10.0,
            retention=5.0,
            payment_deadline_days=30,
            final_payment_conditions="Upon final acceptance"
        ),
        "warranty_period_months": 24,
        "insurance_requirements": "Liability insurance minimum 1M EUR",
        "special_agreements": ["Work according to VOB/B", "Weekly progress reports required"],
        "excluded_services": ["Electrical work", "Plumbing"],
        "penalties": "0.1% of contract value per day of delay, max 5%",
        "quality_standards": "DIN standards apply"
    }