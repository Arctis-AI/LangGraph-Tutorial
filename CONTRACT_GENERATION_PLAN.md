# Subcontractor Contract Draft Generation System - Implementation Plan

## 🎯 Project Overview

A LangGraph-based system to automatically generate subcontractor contract drafts by processing uploaded documents:
- **PDF Files**: Verhandlungsprotokoll (Negotiation Protocol) - contains contract structure and terms
- **Excel Files**: Leistungsverzeichnis (Performance Specifications/Bill of Quantities) - contains detailed work items and pricing

## 🏗️ Contract Generation Flow Architecture

### High-Level Workflow

```
[START]
    ↓
[Upload Handler] → Validate & Store Files
    ↓
[Document Classifier] → Identify document types
    ↓
    ├─→ [PDF Extractor] → Extract negotiation protocol data
    └─→ [Excel Extractor] → Extract performance specifications
            ↓
    [Data Validator] → Validate extracted data
            ↓
    [Data Merger] → Combine data from both sources
            ↓
    [Contract Generator] → Generate draft using template
            ↓
    [Quality Checker] → Review for completeness
            ↓
    [Output Formatter] → Format final contract
            ↓
        [END]
```

## 📊 Detailed Node Specifications

### 1. Upload Handler Node
**Purpose**: Entry point for document processing
- Accepts PDF and Excel files
- Validates file formats and sizes
- Stores files temporarily for processing
- Returns file paths and metadata

### 2. Document Classifier Node
**Purpose**: Route documents to appropriate processors
- Identifies document types (Verhandlungsprotokoll vs Leistungsverzeichnis)
- Routes to appropriate extractors
- Handles missing documents gracefully

### 3. PDF Extractor Node
**Purpose**: Extract structured data from negotiation protocol
- Extracts text from Verhandlungsprotokoll
- Identifies key sections:
  - Contract parties
  - Project description
  - Terms and conditions
  - Payment terms
  - Deadlines
  - Special agreements
- Uses LLM with structured output for intelligent extraction

### 4. Excel Extractor Node
**Purpose**: Extract performance specifications
- Reads Leistungsverzeichnis data
- Extracts:
  - Position numbers
  - Service descriptions
  - Quantities
  - Unit prices
  - Total prices
- Validates numerical data and calculations

### 5. Data Validator Node
**Purpose**: Ensure data integrity
- Checks for required fields
- Validates data consistency
- Flags missing information
- Ensures price calculations are correct

### 6. Data Merger Node
**Purpose**: Combine all extracted information
- Combines protocol and specifications
- Resolves conflicts between sources
- Creates unified contract data structure
- Maps specifications to contract sections

### 7. Contract Generator Node
**Purpose**: Create the actual contract document
- Uses predefined templates
- Inserts extracted data
- Generates contract sections:
  - Preamble
  - Scope of work
  - Performance specifications
  - Payment terms
  - Deadlines
  - Legal terms
  - Appendices

### 8. Quality Checker Node
**Purpose**: Automated quality assurance
- Reviews generated contract
- Checks for:
  - Completeness
  - Consistency
  - Legal requirements
  - Formatting issues
- Generates quality report

### 9. Output Formatter Node
**Purpose**: Prepare final deliverable
- Formats final document
- Supports multiple output formats (DOCX, PDF)
- Adds styling and numbering
- Creates table of contents

## 🔧 Implementation Steps

### Phase 1: Project Setup

#### 1.1 Update Dependencies
Add to `pyproject.toml`:

```toml
[project]
dependencies = [
    # Existing
    "langchain[anthropic]>=0.3.24",
    "langgraph>=0.3.34",
    "python-dotenv>=1.1.0",

    # New additions
    "pdfplumber>=0.11.0",      # PDF extraction
    "openpyxl>=3.1.0",          # Excel processing
    "pandas>=2.2.0",            # Data manipulation
    "python-docx>=1.1.0",       # Word document generation
    "jinja2>=3.1.0",            # Template rendering
    "pydantic>=2.0.0",          # Data validation
    "pypdf>=4.0.0",             # Alternative PDF library
    "reportlab>=4.0.0",         # PDF generation
]
```

#### 1.2 Create Project Structure

```
contract-draft-poc/
├── src/
│   ├── nodes/              # LangGraph nodes
│   │   ├── __init__.py
│   │   ├── upload_handler.py
│   │   ├── document_classifier.py
│   │   ├── pdf_extractor.py
│   │   ├── excel_extractor.py
│   │   ├── data_validator.py
│   │   ├── data_merger.py
│   │   ├── contract_generator.py
│   │   ├── quality_checker.py
│   │   └── output_formatter.py
│   ├── extractors/         # Document extractors
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py
│   │   └── excel_extractor.py
│   ├── validators/         # Data validators
│   │   ├── __init__.py
│   │   └── contract_validator.py
│   ├── templates/          # Contract templates
│   │   ├── base_contract.jinja2
│   │   └── sections/
│   └── models/             # Pydantic models
│       ├── __init__.py
│       ├── state.py
│       └── contract.py
├── data/
│   ├── uploads/            # Uploaded files
│   └── output/             # Generated contracts
├── tests/                  # Test files
│   ├── test_extractors.py
│   ├── test_validators.py
│   └── test_workflow.py
└── config/
    └── settings.py
```

### Phase 2: Core Components

#### 2.1 Define State and Models

```python
# src/models/state.py
from typing import TypedDict, Optional, List, Dict, Any
from typing_extensions import TypedDict

class ContractState(TypedDict):
    # File handling
    uploaded_files: Dict[str, str]  # {file_type: file_path}

    # Extracted data
    verhandlungsprotokoll_data: Optional[Dict[str, Any]]
    leistungsverzeichnis_data: Optional[List[Dict[str, Any]]]

    # Processing data
    merged_data: Optional[Dict[str, Any]]
    contract_draft: Optional[str]

    # Validation and quality
    validation_errors: List[str]
    quality_report: Optional[Dict[str, Any]]

    # Metadata
    processing_status: str
    current_step: str
```

#### 2.2 Pydantic Models for Data Validation

```python
# src/models/contract.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class ContractParty(BaseModel):
    name: str
    address: str
    registration_number: Optional[str]
    contact_person: Optional[str]

class PerformanceItem(BaseModel):
    position_number: str
    description: str
    quantity: float
    unit: str
    unit_price: float
    total_price: float

class ContractData(BaseModel):
    # Parties
    contractor: ContractParty
    subcontractor: ContractParty

    # Project details
    project_name: str
    project_location: str
    project_description: str

    # Performance specifications
    performance_items: List[PerformanceItem]
    total_contract_value: float

    # Terms
    start_date: date
    end_date: date
    payment_terms: str
    warranty_period: Optional[str]

    # Additional clauses
    special_agreements: Optional[List[str]]
```

### Phase 3: LangGraph Implementation

#### 3.1 Main Graph Structure

```python
# src/contract_graph.py
from langgraph.graph import StateGraph, START, END
from src.models.state import ContractState
from src.nodes import *

def create_contract_graph():
    graph = StateGraph(ContractState)

    # Add nodes
    graph.add_node("upload_handler", upload_handler_node)
    graph.add_node("document_classifier", document_classifier_node)
    graph.add_node("pdf_extractor", pdf_extractor_node)
    graph.add_node("excel_extractor", excel_extractor_node)
    graph.add_node("data_validator", data_validator_node)
    graph.add_node("data_merger", data_merger_node)
    graph.add_node("contract_generator", contract_generator_node)
    graph.add_node("quality_checker", quality_checker_node)
    graph.add_node("output_formatter", output_formatter_node)

    # Add edges
    graph.add_edge(START, "upload_handler")
    graph.add_edge("upload_handler", "document_classifier")

    # Parallel extraction
    graph.add_conditional_edges(
        "document_classifier",
        route_documents,
        {
            "both": ["pdf_extractor", "excel_extractor"],
            "pdf_only": "pdf_extractor",
            "excel_only": "excel_extractor"
        }
    )

    # Convergence point
    graph.add_edge("pdf_extractor", "data_validator")
    graph.add_edge("excel_extractor", "data_validator")

    # Sequential processing
    graph.add_edge("data_validator", "data_merger")
    graph.add_edge("data_merger", "contract_generator")
    graph.add_edge("contract_generator", "quality_checker")

    # Conditional edge for quality check
    graph.add_conditional_edges(
        "quality_checker",
        quality_check_router,
        {
            "pass": "output_formatter",
            "fail": "data_validator"  # Retry with corrections
        }
    )

    graph.add_edge("output_formatter", END)

    return graph.compile()
```

### Phase 4: Advanced Features

#### 4.1 Smart Features Implementation
- **Auto-detection of contract type**: Use LLM to classify contract category
- **Intelligent field mapping**: ML-based mapping between different document formats
- **Conflict resolution**: Priority rules and user confirmation for conflicts
- **Multi-language support**: German/English translation and generation

#### 4.2 Validation Rules Engine
- Legal compliance checks against German construction law
- Business rule validation (e.g., payment terms, deadlines)
- Cross-reference validation between documents
- Completeness checks for mandatory fields

#### 4.3 Human-in-the-Loop Integration
- Breakpoints for manual review at critical stages
- UI for data correction and approval
- Feedback loop for continuous improvement
- Audit trail of all changes

### Phase 5: Testing & Deployment

#### 5.1 Test Strategy

```python
# tests/test_workflow.py
import pytest
from src.contract_graph import create_contract_graph

class TestContractGeneration:
    def test_complete_workflow(self):
        """Test full workflow with valid documents"""
        pass

    def test_missing_pdf(self):
        """Test workflow with missing negotiation protocol"""
        pass

    def test_invalid_excel_format(self):
        """Test workflow with malformed Excel file"""
        pass

    def test_data_validation_errors(self):
        """Test handling of validation errors"""
        pass
```

#### 5.2 API Endpoints

```python
# src/api/endpoints.py
from fastapi import FastAPI, UploadFile, File
from typing import List

app = FastAPI()

@app.post("/upload")
async def upload_documents(
    pdf_file: UploadFile = File(None),
    excel_file: UploadFile = File(None)
):
    """Upload contract documents"""
    pass

@app.get("/status/{job_id}")
async def get_processing_status(job_id: str):
    """Check processing status"""
    pass

@app.get("/download/{job_id}")
async def download_contract(job_id: str):
    """Download generated contract"""
    pass
```

## 🎯 Key Implementation Considerations

### 1. Error Handling
- Graceful degradation when documents are incomplete
- Clear, actionable error messages for users
- Retry mechanisms with exponential backoff for LLM calls
- Fallback strategies for extraction failures

### 2. Data Security
- Encrypted file storage
- Secure deletion of temporary files
- API authentication and authorization
- GDPR compliance for personal data

### 3. Scalability
- Async processing for large documents
- Redis caching for extracted data
- Queue-based job processing
- Horizontal scaling capability

### 4. Customization
- Configurable extraction rules per client
- Template library management
- Custom validation rules
- White-labeling support

### 5. Monitoring & Observability
- Structured logging with correlation IDs
- Performance metrics (processing time, success rate)
- LLM token usage tracking
- Error rate monitoring and alerting

## 📈 Success Metrics

1. **Accuracy**: >95% extraction accuracy for structured fields
2. **Processing Time**: <2 minutes for standard documents
3. **Success Rate**: >90% first-time generation success
4. **User Satisfaction**: <10% manual correction required

## 🚀 Next Steps

1. Set up development environment with required dependencies
2. Implement basic node structure and state management
3. Create sample extractors with mock data
4. Build and test the LangGraph workflow
5. Integrate LLM-based extraction
6. Develop contract templates
7. Implement validation and quality checks
8. Create API and UI
9. Conduct user acceptance testing
10. Deploy to production environment

## 📝 Notes

- Consider using GPT-4 or Claude for complex German legal text extraction
- Implement versioning for contract templates
- Plan for regulatory compliance updates
- Consider integration with existing ERP/CRM systems
- Build comprehensive documentation for end-users