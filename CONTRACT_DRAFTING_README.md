# General Contract Drafting System

AI-powered construction contract drafting system that generates contracts from predefined types, project descriptions, and supporting documents.

## Features

✅ **94 Predefined Contract Types** - From subcontracts to EPC agreements
✅ **Document Extraction** - Processes PDF/DOCX (Verhandlungsprotokoll) and Excel (Leistungsverzeichnis)
✅ **Knowledge Base Integration** - Learns from historical contracts (optional)
✅ **Intelligent Structure Building** - Creates contract outlines based on type requirements
✅ **Automated Clause Generation** - Generates German legal text with LLM
✅ **Quality Assessment** - Scores and validates generated contracts
✅ **Multiple Output Formats** - TXT, DOCX, and JSON quality reports

## Architecture

### Workflow (9 Nodes)

```
User Input → Document Extract → KB Fetch → Structure Build → Content Map
→ Clause Generate → Consistency Check → Quality Review → Output Format
```

### Nodes

1. **User Input Handler** - Loads contract type, validates inputs
2. **Document Extractor** - Extracts from PDF/DOCX (Verhandlungsprotokoll)
3. **Excel Extractor** - Extracts from Excel (Leistungsverzeichnis)
4. **Knowledge Base Fetcher** - Retrieves historical contracts/clauses (graceful degradation)
5. **Structure Analyzer** - Builds hierarchical contract outline
6. **Content Mapper** - Maps extracted data to sections
7. **Clause Generator** - Generates sections with LLM
8. **Consistency Checker** - Validates cross-references and data
9. **Quality Reviewer** - Assesses quality and completeness
10. **Output Formatter** - Generates TXT, DOCX, and reports

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Optional: Set up Supabase credentials for knowledge base
export SUPABASE_URL="your-supabase-url"
export SUPABASE_KEY="your-supabase-key"

# Knowledge base is optional - system works without it
```

## Usage

### Quick Start

```python
from src.contract_drafting_graph import create_contract_drafting_graph

# Initialize workflow
graph = create_contract_drafting_graph()

# Prepare input
initial_state = {
    # Select contract type (from 94 available types)
    "contract_type_id": "00827bca-eccf-4e5a-87bb-dcd438c4ff29",  # Site Supervision

    # Describe project
    "project_description": "Site supervision for office building in Berlin...",

    # Upload documents (optional)
    "uploaded_documents": [
        {"type": "verhandlungsprotokoll", "path": "data/vp.pdf"},
        {"type": "leistungsverzeichnis", "path": "data/lv.xlsx"}
    ],

    # Initialize required fields
    "messages": [],
    "errors": [],
    # ... (see examples/run_contract_drafting.py for complete example)
}

# Run workflow
result = graph.invoke(initial_state, config={"configurable": {"thread_id": "1"}})

# Access results
print(f"Quality Score: {result['quality_score']}")
print(f"Output Files: {result['output_files']}")
print(f"Contract Draft: {result['contract_draft'][:500]}...")
```

### Running the Example

```bash
python examples/run_contract_drafting.py
```

## Contract Types

The system includes 94 contract types organized hierarchically:

- **MAIN** - Main contracts (Traditional, Design-Build, EPC, etc.)
- **SUBCONTRACT** - Subcontracts (Trade, Service, Supplier)
- **PROF_TECH** - Professional services (Architecture, Engineering, Quantity Surveying)
- **PROC_SUPPLY** - Procurement (Framework, Long-term, Spot Purchase)
- **BONDS_INS** - Bonds and Insurance
- **ANCILLARY** - Supporting agreements (NDA, SLA, etc.)

Each type includes:
- Required sections
- Policy templates
- Example clauses (in German, English, French)
- Jurisdiction information

## File Structure

```
src/
├── models/
│   ├── contract_drafting_state.py   # State model
│   └── contract.py                   # Data models
├── nodes/
│   └── contract_drafting/           # New drafting nodes
│       ├── user_input_handler.py
│       ├── knowledge_base_fetcher.py
│       ├── structure_analyzer.py
│       ├── content_mapper.py
│       ├── clause_generator.py
│       ├── consistency_checker.py
│       ├── quality_reviewer.py
│       └── output_formatter.py
├── contract_drafting_graph.py       # Main workflow
└── prompts/                          # LLM prompts

knowledge_base/
└── contract_types/
    └── contract_types_rows.json     # 94 contract type definitions

examples/
└── run_contract_drafting.py         # Usage example

data/
├── uploads/                          # Input documents
└── output/                           # Generated contracts
```

## Configuration

### Environment Variables

```bash
# LLM Configuration (required)
ANTHROPIC_API_KEY=your-key           # For Claude models
OPENAI_API_KEY=your-key              # Alternative: OpenAI

# Supabase (optional - for knowledge base)
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# If Supabase is not configured, system generates contracts without historical examples
```

### Knowledge Base (Optional)

The system can optionally fetch historical contracts and clauses from Supabase:

**Tables needed:**
- `contracts` - Historical contracts with `contract_type_code`
- `clauses` - Extracted clauses with `contract_type_code`
- `contract_structures` - Learned structures

**Graceful Degradation:**
If Supabase is unavailable:
- ✅ Workflow continues without error
- ✅ Uses contract type `required_sections` for outline
- ✅ Generates clauses without historical examples
- ✅ Quality may be slightly lower

## Output

### Generated Files

1. **TXT File** - Plain text contract
2. **DOCX File** - Formatted Word document with:
   - Professional formatting
   - Section headings
   - Highlighted review markers
   - Quality report page
3. **JSON Report** - Quality metrics and issues

### Quality Scoring

Scores (0-100) based on:
- ✅ Section completeness
- ✅ Data usage from documents
- ✅ Consistency (no conflicts)
- ✅ Length and detail
- ⚠️ Issues found

**Levels:**
- 85-100: Excellent
- 70-84: Good
- 50-69: Fair (manual review recommended)
- 0-49: Poor (major issues)

## Examples

### Example 1: Site Supervision with Documents

```python
initial_state = {
    "contract_type_id": "00827bca-eccf-4e5a-87bb-dcd438c4ff29",
    "project_description": "Site supervision for office building...",
    "uploaded_documents": [
        {"type": "verhandlungsprotokoll", "path": "data/vp.pdf"},
        {"type": "leistungsverzeichnis", "path": "data/lv.xlsx"}
    ],
    # ... init fields
}

result = graph.invoke(initial_state)
# → Generates contract with extracted data
```

### Example 2: EPC Contract without Documents

```python
initial_state = {
    "contract_type_id": "0421cc2f-ccab-4867-960e-f79aaa9f7bbd",  # EPC
    "project_description": "Engineering, procurement, and construction for power plant...",
    "uploaded_documents": [],  # No documents
    # ... init fields
}

result = graph.invoke(initial_state)
# → Generates template contract from contract type requirements
```

## Advanced Usage

### Custom Contract Types

Add new contract types to `knowledge_base/contract_types/contract_types_rows.json`:

```json
{
  "id": "new-uuid",
  "code": "CUSTOM_TYPE",
  "name": "Custom Contract Type",
  "name_de": "Benutzerdefinierter Vertragstyp",
  "required_sections": [
    "Scope of Work",
    "Payment Terms",
    "Duration"
  ],
  "policies": {
    "de": {
      "policy_key": "policy_value"
    }
  }
}
```

### Extending the Workflow

Add custom nodes by:
1. Creating node function in `src/nodes/contract_drafting/`
2. Updating graph in `src/contract_drafting_graph.py`
3. Adding to state model if needed

## Troubleshooting

### Common Issues

**Issue**: Contract type not found
**Solution**: Check that `contract_type_id` exists in `contract_types_rows.json`

**Issue**: Document extraction fails
**Solution**: Verify file paths and formats (PDF/DOCX/TXT for VP, XLSX/CSV for LV)

**Issue**: Knowledge base unavailable
**Solution**: This is expected if Supabase not configured - workflow continues normally

**Issue**: Low quality score
**Solution**:
- Add more project description detail
- Upload supporting documents
- Manually review and edit generated sections

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Roadmap

- [ ] Multi-language support (currently German-focused)
- [ ] Interactive editing UI
- [ ] More document types (CAD drawings, correspondence)
- [ ] Clause recommendation engine
- [ ] Version control and comparison
- [ ] Collaboration features

## Contributing

1. Add new contract types to knowledge base
2. Improve prompts in `src/prompts/`
3. Enhance extraction logic for specific document formats
4. Add quality checks to consistency checker

## License

[Your License]

## Support

For issues and questions:
- GitHub Issues: [Your Repo]
- Documentation: See `FINAL_ARCHITECTURE.md` for detailed design

---

**Generated with LangGraph + Claude**
