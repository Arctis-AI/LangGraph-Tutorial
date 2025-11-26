# Quick Start Guide

Get started with the Contract Drafting System in 3 simple steps!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set Up Environment

```bash
# Required: LLM API Key
export ANTHROPIC_API_KEY="your-anthropic-key"
# or
export OPENAI_API_KEY="your-openai-key"

# Optional: Supabase (for knowledge base)
export SUPABASE_URL="your-supabase-url"
export SUPABASE_KEY="your-supabase-key"
```

Or create a `.env` file:
```env
ANTHROPIC_API_KEY=your-key-here
# SUPABASE_URL=...
# SUPABASE_KEY=...
```

## 3. Run the System

### Option A: Using Main Script (Simplest)

```bash
# Use default settings (Site Supervision contract)
python main.py

# With custom project description
python main.py --description "Supervision for Berlin office building project..."

# With documents
python main.py --pdf data/vp.pdf --excel data/lv.xlsx

# With specific contract type
python main.py --contract-type "0421cc2f-ccab-4867-960e-f79aaa9f7bbd"
```

### Option B: Using Example Script

```bash
python examples/run_contract_drafting.py
```

### Option C: Python API

```python
from src.contract_drafting_graph import create_contract_drafting_graph
from datetime import datetime

# Create workflow
graph = create_contract_drafting_graph()

# Prepare state
state = {
    "contract_type_id": "00827bca-eccf-4e5a-87bb-dcd438c4ff29",  # Site Supervision
    "project_description": "Your project description here...",
    "uploaded_documents": [],  # Optional
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

# Run
result = graph.invoke(state, config={"configurable": {"thread_id": "1"}})

# Check results
print(f"Quality: {result['quality_score']:.1f}/100")
print(f"Files: {result['output_files']}")
```

## Output

Generated files in `data/output/`:
- `contract_XXXX_timestamp.txt` - Plain text contract
- `contract_XXXX_timestamp.docx` - Formatted Word document
- `quality_report_timestamp.json` - Quality assessment

## Contract Types

Browse available contract types:

```python
import json
with open("knowledge_base/contract_types/contract_types_rows.json") as f:
    types = json.load(f)
    for t in types[:10]:
        print(f"{t['id']}: {t['name']} ({t['name_de']})")
```

### Popular Types

| ID | Name | Code |
|----|------|------|
| `00827bca-...` | Site Supervision Subcontract | SITE_SUPERVISION |
| `0421cc2f-...` | EPC Contract | EPC |
| `151a8ef1-...` | Design-Bid-Build | DESIGN_BID_BUILD |

## Troubleshooting

**Problem**: "Contract type not found"
**Solution**: Check ID in `contract_types_rows.json`

**Problem**: "No LLM API key"
**Solution**: Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`

**Problem**: "Knowledge base unavailable"
**Solution**: This is OK! System works without Supabase

**Problem**: Low quality score
**Solution**:
- Add more detailed project description
- Upload supporting documents
- Manually review generated sections

## Next Steps

- Read [CONTRACT_DRAFTING_README.md](CONTRACT_DRAFTING_README.md) for full documentation
- See [FINAL_ARCHITECTURE.md](FINAL_ARCHITECTURE.md) for architecture details
- Check `examples/` for more usage examples

## Support

Need help? Check:
- Documentation in `/docs`
- Architecture guides
- Example scripts in `/examples`

---

**Ready to generate your first contract? Run:**
```bash
python main.py
```
