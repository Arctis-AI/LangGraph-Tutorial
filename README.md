# Subcontractor Contract Generation System

An intelligent contract generation system built with LangGraph that automatically creates subcontractor agreements from negotiation protocols and bills of quantities.

## 🎯 Overview

This system processes two key documents to generate comprehensive subcontractor contracts:
- **Verhandlungsprotokoll** (Negotiation Protocol) - Contains contract terms, parties, and conditions
- **Leistungsverzeichnis** (Bill of Quantities) - Contains detailed work items and pricing

## 🏗️ Architecture

The system uses a LangGraph workflow with the following nodes:

```
Upload Handler → Document Classifier → PDF Extractor → Excel Extractor
→ Data Validator → Data Merger → Contract Generator → Quality Checker
→ Output Formatter
```

## 📦 Features

- **Intelligent Document Processing**: Uses LLM to extract structured data from unstructured PDFs
- **Excel Data Extraction**: Automatically parses performance items and pricing from spreadsheets
- **Data Validation**: Validates extracted data for completeness and consistency
- **Smart Merging**: Combines data from multiple sources intelligently
- **Template-Based Generation**: Uses Jinja2 templates for flexible contract formatting
- **Quality Assurance**: Built-in quality checks ensure contract completeness
- **Multi-Format Output**: Generates both DOCX and TXT versions

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd contract-draft-poc

# Install dependencies using uv
uv add -r pyproject.toml
```

### Usage

1. Place your documents in the `resources` folder:
   - `verhandlungsprotokoll.pdf` or `verhandlungsprotokoll.txt`
   - `leistungsverzeichnis.xlsx`

2. Run the contract generation:

```bash
uv run python main.py
```

3. Find generated contracts in `data/output/`

## 📁 Project Structure

```
contract-draft-poc/
├── src/
│   ├── nodes/              # LangGraph workflow nodes
│   ├── models/             # Pydantic data models
│   ├── templates/          # Contract templates (Jinja2)
│   └── contract_graph.py   # Main workflow definition
├── resources/              # Input documents
├── data/output/           # Generated contracts
└── main.py                # Entry point
```

## 🔧 Configuration

Set your API key in `.env`:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

## 📊 Workflow Details

### 1. Upload Handler
- Loads documents from the resources folder
- Validates file existence

### 2. Document Classifier
- Identifies available document types
- Routes to appropriate extractors

### 3. PDF Extractor
- Extracts text from PDF/TXT files
- Uses Claude to structure unstructured data
- Extracts: parties, dates, terms, conditions

### 4. Excel Extractor
- Reads bill of quantities from Excel
- Extracts: items, quantities, prices
- Calculates totals and taxes

### 5. Data Validator
- Validates required fields
- Checks date consistency
- Verifies price calculations

### 6. Data Merger
- Combines data from all sources
- Resolves conflicts
- Creates unified contract structure

### 7. Contract Generator
- Renders contract using Jinja2 template
- Supports bilingual format (German/English)

### 8. Quality Checker
- Verifies contract completeness
- Checks for required sections
- Generates quality score

### 9. Output Formatter
- Saves as TXT and DOCX
- Formats document professionally

## 📈 Sample Output

The system generates professional contracts including:
- Contract parties with full details
- Project description and location
- Detailed bill of quantities
- Payment terms and schedules
- Warranties and penalties
- Legal terms and conditions

## 🛠️ Customization

### Adding New Fields

1. Update the Pydantic models in `src/models/contract.py`
2. Modify the extraction prompts in extractor nodes
3. Update the Jinja2 template in `src/templates/`

### Changing Templates

Edit `src/templates/contract_template.jinja2` to customize the contract format.

## 🧪 Testing

Run the test workflow:

```bash
uv run python main.py --verbose
```

## 📝 Notes

- The system uses Claude Sonnet for intelligent data extraction
- Default VAT rate is set to 19% (German standard)
- Contracts follow VOB/B standards
- All amounts are in EUR by default

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

[Your License Here]