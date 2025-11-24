"""Contract data models for validation and structure."""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import date
from decimal import Decimal


class ContractParty(BaseModel):
    """Represents a party in the contract (contractor/subcontractor)."""

    name: str = Field(..., description="Company name")
    address: str = Field(..., description="Full address")
    registration_number: Optional[str] = Field(None, description="Company registration number")
    tax_id: Optional[str] = Field(None, description="Tax identification number")
    contact_person: Optional[str] = Field(None, description="Primary contact person")
    email: Optional[str] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone number")


class PerformanceItem(BaseModel):
    """Represents a single performance item/position from Leistungsverzeichnis."""

    position_number: str = Field(..., description="Position/item number")
    description: str = Field(..., description="Description of work/service")
    quantity: float = Field(..., description="Quantity")
    unit: str = Field(..., description="Unit of measurement")
    unit_price: float = Field(..., description="Price per unit")
    total_price: float = Field(..., description="Total price for this item")
    notes: Optional[str] = Field(None, description="Additional notes")

    @field_validator('total_price')
    @classmethod
    def validate_total_price(cls, v: float, values: Dict[str, Any]) -> float:
        """Validate that total price matches quantity * unit_price."""
        if 'quantity' in values.data and 'unit_price' in values.data:
            expected = round(values.data['quantity'] * values.data['unit_price'], 2)
            if abs(v - expected) > 0.01:  # Allow for small rounding differences
                # Auto-correct the total price
                return expected
        return v


class PaymentTerms(BaseModel):
    """Payment terms structure."""

    payment_schedule: str = Field(..., description="Payment schedule description")
    advance_payment: Optional[float] = Field(None, description="Advance payment percentage")
    retention: Optional[float] = Field(None, description="Retention percentage")
    payment_deadline_days: int = Field(30, description="Days for payment after invoice")
    final_payment_conditions: Optional[str] = Field(None, description="Conditions for final payment")


class VerhandlungsprotokollData(BaseModel):
    """Structured data extracted from Verhandlungsprotokoll (negotiation protocol)."""

    project_name: str = Field(..., description="Project name")
    project_location: str = Field(..., description="Project location/address")
    project_description: str = Field(..., description="Detailed project description")

    contractor: ContractParty = Field(..., description="Main contractor details")
    subcontractor: ContractParty = Field(..., description="Subcontractor details")

    negotiation_date: Optional[date] = Field(None, description="Date of negotiation")
    contract_start_date: date = Field(..., description="Contract start date")
    contract_end_date: date = Field(..., description="Contract end date")

    scope_of_work: str = Field(..., description="Detailed scope of work")
    payment_terms: PaymentTerms = Field(..., description="Payment terms")

    warranty_period_months: Optional[int] = Field(None, description="Warranty period in months")
    insurance_requirements: Optional[str] = Field(None, description="Required insurances")

    special_agreements: List[str] = Field(default_factory=list, description="Special agreements")
    excluded_services: List[str] = Field(default_factory=list, description="Explicitly excluded services")

    penalties: Optional[str] = Field(None, description="Penalty clauses")
    quality_standards: Optional[str] = Field(None, description="Required quality standards")


class LeistungsverzeichnisData(BaseModel):
    """Structured data extracted from Leistungsverzeichnis (bill of quantities)."""

    document_title: str = Field(..., description="Title of the document")
    project_reference: Optional[str] = Field(None, description="Project reference number")
    creation_date: Optional[date] = Field(None, description="Document creation date")

    performance_items: List[PerformanceItem] = Field(..., description="List of performance items")

    subtotal: float = Field(..., description="Sum before taxes")
    tax_rate: float = Field(0.19, description="Tax rate (default 19% for Germany)")
    tax_amount: float = Field(..., description="Tax amount")
    total_amount: float = Field(..., description="Total including tax")

    currency: str = Field("EUR", description="Currency")
    notes: Optional[str] = Field(None, description="Additional notes")

    @field_validator('total_amount')
    @classmethod
    def validate_total_amount(cls, v: float, values: Dict[str, Any]) -> float:
        """Validate that total amount matches subtotal + tax."""
        if 'subtotal' in values.data and 'tax_amount' in values.data:
            expected = round(values.data['subtotal'] + values.data['tax_amount'], 2)
            if abs(v - expected) > 0.01:
                return expected
        return v


class ContractData(BaseModel):
    """Complete contract data after merging all sources."""

    # Parties
    contractor: ContractParty
    subcontractor: ContractParty

    # Project details
    project_name: str
    project_location: str
    project_description: str
    project_reference: Optional[str] = None

    # Dates
    contract_date: date
    start_date: date
    end_date: date

    # Scope and specifications
    scope_of_work: str
    performance_items: List[PerformanceItem]
    excluded_services: List[str] = Field(default_factory=list)

    # Financial
    subtotal: float
    tax_rate: float
    tax_amount: float
    total_contract_value: float
    currency: str = "EUR"

    # Terms and conditions
    payment_terms: PaymentTerms
    warranty_period_months: Optional[int] = None
    insurance_requirements: Optional[str] = None
    penalties: Optional[str] = None
    quality_standards: Optional[str] = None

    # Additional
    special_agreements: List[str] = Field(default_factory=list)
    attachments: List[str] = Field(default_factory=list)

    # Metadata
    generated_date: date = Field(default_factory=date.today)
    version: str = "1.0"