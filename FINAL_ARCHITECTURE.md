# Construction Contract Drafting - Final LangGraph Architecture

## Overview
General construction contract drafting system that works entirely in-memory with state-based data flow. No database schema changes needed - simply fetch data from Supabase and work with it in the LangGraph state.

---

## Key Principles

1. ✅ **No Supabase schema creation** - Use existing tables as-is
2. ✅ **State-based workflow** - All data flows through LangGraph state
3. ✅ **Simple data fetching** - Query Supabase, store in state, process
4. ✅ **Contract types predefined** - Use existing 94 types from knowledge base
5. ✅ **Two document types** - Leistungsverzeichnis (Excel) + Verhandlungsprotokoll (PDF/DOCX)

---

## LangGraph Flow (Simplified)

```
START
  │
  ├──> [1] USER_INPUT_HANDLER
  │    Input: Contract type selection, project description, documents
  │    Output: State with user inputs
  │
  ├──> [2] DOCUMENT_EXTRACTOR (Parallel)
  │    Input: Uploaded documents
  │    Output: Extracted data in state
  │    • PDF/DOCX → verhandlungsprotokoll_data
  │    • Excel → leistungsverzeichnis_data
  │
  ├──> [3] KNOWLEDGE_BASE_FETCHER (Optional - can be skipped)
  │    Input: Contract type code, project description
  │    Output: Retrieved contracts, clauses, structures in state
  │    • Query Supabase for similar contracts
  │    • Fetch example clauses
  │    • Get contract structures
  │    • Store everything in state
  │    • If fetch fails → Skip this node and continue
  │
  ├──> [4] STRUCTURE_ANALYZER
  │    Input: Contract type + retrieved structures
  │    Output: Contract outline in state
  │    • Use required_sections from contract type
  │    • Analyze historical structures
  │    • Build proposed outline
  │
  ├──> [5] CONTENT_MAPPER
  │    Input: Outline + extracted data
  │    Output: Section mappings in state
  │    • Map data to sections
  │    • Calculate completeness
  │    • Identify gaps
  │
  ├──> [6] CLAUSE_GENERATOR
  │    Input: Outline + mappings + retrieved clauses
  │    Output: Generated sections in state
  │    • Generate section by section
  │    • Use examples as references
  │    • Fill with extracted data
  │
  ├──> [7] CONSISTENCY_CHECKER
  │    Input: Generated contract draft
  │    Output: Consistency issues in state
  │    • Check cross-references
  │    • Validate data consistency
  │
  ├──> [8] QUALITY_REVIEWER
  │    Input: Contract draft + consistency issues
  │    Output: Quality report in state
  │    • Score quality
  │    • Identify gaps
  │
  └──> [9] OUTPUT_FORMATTER
       Input: Final draft + quality report
       Output: Files (DOCX, PDF, Report)
       END
```

---

## State Schema

```python
from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime

class ContractDraftingState(TypedDict):
    # ===== [1] User Inputs =====
    contract_type_id: str
    contract_type_code: str  # e.g., "SITE_SUPERVISION"
    contract_type_data: Dict[str, Any]  # Full contract type object from JSON
    project_description: str
    uploaded_documents: List[Dict[str, str]]

    # ===== [2] Extracted Data =====
    verhandlungsprotokoll_data: Optional[Dict[str, Any]]
    leistungsverzeichnis_data: Optional[Dict[str, Any]]

    # ===== [3] Knowledge Base Data (fetched from Supabase) =====
    retrieved_contracts: List[Dict[str, Any]]  # Similar contracts
    retrieved_clauses: List[Dict[str, Any]]    # Example clauses
    contract_structures: List[Dict[str, Any]]  # Structure examples

    # ===== [4] Structure =====
    contract_outline: List[Dict[str, Any]]  # Hierarchical outline

    # ===== [5] Content Mapping =====
    section_mappings: Dict[str, Dict[str, Any]]  # Data → Sections

    # ===== [6] Generation =====
    generated_sections: Dict[str, str]  # Section number → text
    contract_draft: str  # Full contract text

    # ===== [7] Consistency =====
    consistency_issues: List[Dict[str, Any]]

    # ===== [8] Quality =====
    quality_report: Dict[str, Any]
    quality_score: float

    # ===== [9] Output =====
    output_files: Dict[str, str]

    # ===== Status & Logging =====
    current_step: str
    messages: List[Dict[str, str]]
    errors: List[str]
```

---

## Node Implementations

### [1] User Input Handler

**Purpose**: Collect and validate user inputs

```python
def user_input_handler_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Handle user inputs: contract type selection, description, documents.
    """
    print("📝 Processing user inputs...")

    updates = {
        "current_step": "user_input_handler",
        "messages": []
    }

    # Load contract type data from JSON
    contract_type_id = state.get("contract_type_id")
    contract_types = load_contract_types()  # Load from contract_types_rows.json

    contract_type_data = next(
        (ct for ct in contract_types if ct["id"] == contract_type_id),
        None
    )

    if not contract_type_data:
        updates["errors"] = [f"Contract type {contract_type_id} not found"]
        return updates

    updates["contract_type_data"] = contract_type_data
    updates["contract_type_code"] = contract_type_data["code"]

    updates["messages"].append({
        "role": "system",
        "content": f"✓ Contract type selected: {contract_type_data['name']}"
    })

    # Validate documents
    uploaded_docs = state.get("uploaded_documents", [])
    if not uploaded_docs:
        updates["messages"].append({
            "role": "system",
            "content": "⚠️ No documents uploaded"
        })

    return updates


def load_contract_types() -> List[Dict[str, Any]]:
    """Load contract types from JSON file."""
    import json
    with open("knowledge_base/contract_types/contract_types_rows.json", "r") as f:
        return json.load(f)
```

---

### [2] Document Extractor

**Reuse existing extractors** - No changes needed!

```python
def document_extraction_router(state: ContractDraftingState):
    """
    Route to document and excel extractors in parallel.
    Both extractors already implemented - just use them.
    """
    # The existing document_extractor_node and excel_extractor_node
    # already populate state with:
    # - verhandlungsprotokoll_data
    # - leistungsverzeichnis_data
    pass
```

---

### [3] Knowledge Base Fetcher

**Purpose**: Fetch data from Supabase and store in state

```python
from supabase import create_client, Client

def knowledge_base_fetcher_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Fetch relevant contracts, clauses, and structures from Supabase.
    Store everything in state.

    If fetch fails, returns empty data and continues workflow without error.
    """
    print("🔍 Fetching knowledge base data...")

    updates = {
        "current_step": "knowledge_base_fetcher",
        "messages": [],
        # Set defaults in case of failure
        "retrieved_contracts": [],
        "retrieved_clauses": [],
        "contract_structures": []
    }

    try:
        # Initialize Supabase client
        supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )

        contract_type_code = state.get("contract_type_code")
        project_description = state.get("project_description", "")

        # 1. Fetch similar contracts by type
        contracts_response = supabase.table("contracts") \
            .select("*") \
            .eq("contract_type_code", contract_type_code) \
            .limit(5) \
            .execute()

        updates["retrieved_contracts"] = contracts_response.data or []

        # 2. Fetch example clauses for this contract type
        clauses_response = supabase.table("clauses") \
            .select("*") \
            .eq("contract_type_code", contract_type_code) \
            .limit(20) \
            .execute()

        updates["retrieved_clauses"] = clauses_response.data or []

        # 3. Fetch contract structures
        structures_response = supabase.table("contract_structures") \
            .select("*") \
            .eq("contract_type_code", contract_type_code) \
            .execute()

        updates["contract_structures"] = structures_response.data or []

        # 4. Optional: Semantic search by project description
        # If you have embeddings set up
        if project_description:
            # embedding = get_embedding(project_description)
            # semantic_results = supabase.rpc("match_contracts", {
            #     "query_embedding": embedding,
            #     "match_threshold": 0.7,
            #     "match_count": 5
            # }).execute()
            # Merge with retrieved_contracts
            pass

        updates["messages"].append({
            "role": "system",
            "content": f"✓ Retrieved {len(updates['retrieved_contracts'])} contracts, "
                      f"{len(updates['retrieved_clauses'])} clauses"
        })

    except Exception as e:
        # Log the error but don't fail the workflow
        print(f"⚠️ Knowledge base fetch failed: {str(e)}")
        updates["messages"].append({
            "role": "system",
            "content": f"⚠️ Knowledge base unavailable - proceeding without historical examples"
        })
        # Empty defaults already set above

    return updates
```

---

### [4] Structure Analyzer

**Purpose**: Build contract outline using contract type + historical structures

```python
from src.core.llm_clients import get_llm_client

def structure_analyzer_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Analyze contract structures and build outline.
    """
    print("📋 Analyzing contract structure...")

    updates = {
        "current_step": "structure_analyzer",
        "messages": []
    }

    contract_type_data = state.get("contract_type_data", {})
    required_sections = contract_type_data.get("required_sections", [])
    retrieved_structures = state.get("contract_structures", [])
    project_description = state.get("project_description", "")

    llm = get_llm_client()

    # Build structure analysis prompt
    prompt = f"""
Analyze and create a contract outline for: {contract_type_data.get('name')}

Required Sections (mandatory):
{json.dumps(required_sections, indent=2)}

Historical Structures (examples):
{json.dumps(retrieved_structures[:3], indent=2) if retrieved_structures else "No historical data"}

Project Description:
{project_description}

Available Data:
- Verhandlungsprotokoll: {bool(state.get('verhandlungsprotokoll_data'))}
- Leistungsverzeichnis: {bool(state.get('leistungsverzeichnis_data'))}

Task:
Create a hierarchical contract outline with:
1. All mandatory sections from required_sections
2. Optional relevant sections based on project
3. For each section:
   - section_number (e.g., "§1", "§2")
   - title_de (German title)
   - title_en (English title)
   - description (what should be included)
   - mandatory (true/false)
   - priority (1=highest)

Return as JSON array of sections.
"""

    try:
        response = llm.invoke([
            {"role": "system", "content": "You are a contract structure expert. Return valid JSON only."},
            {"role": "user", "content": prompt}
        ])

        # Parse JSON response
        outline_text = response.content
        if "```json" in outline_text:
            outline_text = outline_text.split("```json")[1].split("```")[0]

        import json
        contract_outline = json.loads(outline_text.strip())

        updates["contract_outline"] = contract_outline
        updates["messages"].append({
            "role": "system",
            "content": f"✓ Created outline with {len(contract_outline)} sections"
        })

    except Exception as e:
        updates["errors"] = [f"Structure analysis failed: {str(e)}"]
        # Fallback: use required_sections directly
        updates["contract_outline"] = [
            {
                "section_number": f"§{i+1}",
                "title_de": section,
                "title_en": section,
                "mandatory": True,
                "priority": i+1
            }
            for i, section in enumerate(required_sections)
        ]

    return updates
```

---

### [5] Content Mapper

**Purpose**: Map extracted data to outline sections

```python
def content_mapper_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Map extracted data to contract sections.
    """
    print("🗺️ Mapping content to sections...")

    updates = {
        "current_step": "content_mapper",
        "messages": []
    }

    outline = state.get("contract_outline", [])
    vp_data = state.get("verhandlungsprotokoll_data", {})
    lv_data = state.get("leistungsverzeichnis_data", {})

    section_mappings = {}

    for section in outline:
        section_num = section["section_number"]
        section_title = section.get("title_de", "")

        mapping = {
            "section_number": section_num,
            "title": section_title,
            "available_data": [],
            "missing_data": [],
            "completeness": 0.0,
            "priority": section.get("priority", 999)
        }

        # Simple mapping logic based on section content
        title_lower = section_title.lower()

        # Scope/Work sections
        if any(keyword in title_lower for keyword in ["leistung", "scope", "work"]):
            if vp_data.get("scope_of_work"):
                mapping["available_data"].append("scope_of_work")
            if lv_data.get("performance_items"):
                mapping["available_data"].append("performance_items")

        # Payment sections
        if any(keyword in title_lower for keyword in ["vergütung", "payment", "zahlung"]):
            if vp_data.get("payment_terms"):
                mapping["available_data"].append("payment_terms")
            if lv_data.get("total_amount"):
                mapping["available_data"].append("total_amount")

        # Parties sections
        if any(keyword in title_lower for keyword in ["partei", "parties", "vertragspartner"]):
            if vp_data.get("contractor"):
                mapping["available_data"].append("contractor")
            if vp_data.get("subcontractor"):
                mapping["available_data"].append("subcontractor")

        # Dates/Timeline sections
        if any(keyword in title_lower for keyword in ["frist", "termin", "deadline", "date"]):
            if vp_data.get("contract_start_date"):
                mapping["available_data"].append("contract_start_date")
            if vp_data.get("contract_end_date"):
                mapping["available_data"].append("contract_end_date")

        # Calculate completeness
        if len(mapping["available_data"]) > 0:
            mapping["completeness"] = min(1.0, len(mapping["available_data"]) * 0.3)

        section_mappings[section_num] = mapping

    updates["section_mappings"] = section_mappings
    updates["messages"].append({
        "role": "system",
        "content": f"✓ Mapped data to {len(section_mappings)} sections"
    })

    return updates
```

---

### [6] Clause Generator

**Purpose**: Generate contract sections using data + examples

```python
def clause_generator_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Generate contract sections iteratively.
    """
    print("✍️ Generating contract clauses...")

    updates = {
        "current_step": "clause_generator",
        "messages": [],
        "generated_sections": {},
        "contract_draft": ""
    }

    outline = state.get("contract_outline", [])
    section_mappings = state.get("section_mappings", {})
    retrieved_clauses = state.get("retrieved_clauses", [])
    vp_data = state.get("verhandlungsprotokoll_data", {}) or {}
    lv_data = state.get("leistungsverzeichnis_data", {}) or {}
    contract_type_data = state.get("contract_type_data", {})

    llm = get_llm_client()
    generated_sections = {}

    # Sort by priority
    sorted_outline = sorted(outline, key=lambda x: x.get("priority", 999))

    for section in sorted_outline:
        section_num = section["section_number"]
        section_title = section["title_de"]

        # Get mapping for this section
        mapping = section_mappings.get(section_num, {})

        # Get relevant data
        section_data = {}
        for data_key in mapping.get("available_data", []):
            if data_key in vp_data:
                section_data[data_key] = vp_data[data_key]
            elif data_key in lv_data:
                section_data[data_key] = lv_data[data_key]

        # Get relevant example clauses
        relevant_clauses = [
            c for c in retrieved_clauses
            if section_title.lower() in c.get("section_title", "").lower()
        ][:3]

        # Generate section
        prompt = f"""
Generate contract section: {section_title} ({section_num})

Contract Type: {contract_type_data.get('name')}

Section Description:
{section.get('description', 'Standard construction contract section')}

Available Data:
{json.dumps(section_data, indent=2, default=str)}

Example Clauses (reference style and structure):
{json.dumps([c.get('clause_text', '')[:500] for c in relevant_clauses], indent=2) if relevant_clauses else "No examples"}

Previously Generated Sections (for context):
{json.dumps({k: v[:200] + "..." for k, v in list(generated_sections.items())[-2:]}, indent=2) if generated_sections else "None"}

Instructions:
1. Write in German legal language
2. Use provided data where available
3. Follow structure from examples
4. Be specific and clear
5. Mark gaps with [REVIEW NEEDED: reason]
6. Keep consistent with previous sections

Generate ONLY the section text (no explanations).
"""

        try:
            response = llm.invoke([
                {"role": "system", "content": "You are a contract drafting expert. Write precise German legal text."},
                {"role": "user", "content": prompt}
            ])

            section_text = response.content.strip()
            generated_sections[section_num] = section_text

        except Exception as e:
            generated_sections[section_num] = f"[ERROR GENERATING SECTION: {str(e)}]"

    # Compile full contract
    contract_draft = ""
    for section in sorted_outline:
        section_num = section["section_number"]
        section_title = section["title_de"]
        section_text = generated_sections.get(section_num, "[NOT GENERATED]")

        contract_draft += f"\n\n{section_num} {section_title}\n\n{section_text}"

    updates["generated_sections"] = generated_sections
    updates["contract_draft"] = contract_draft
    updates["messages"].append({
        "role": "system",
        "content": f"✓ Generated {len(generated_sections)} sections"
    })

    return updates
```

---

### [7] Consistency Checker

**Purpose**: Validate contract coherence

```python
def consistency_checker_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Check contract consistency.
    """
    print("✅ Checking consistency...")

    updates = {
        "current_step": "consistency_checker",
        "messages": [],
        "consistency_issues": []
    }

    contract_draft = state.get("contract_draft", "")
    issues = []

    # 1. Check cross-references
    import re
    references = re.findall(r'§\d+', contract_draft)
    for ref in set(references):
        if ref not in contract_draft.split(ref)[0]:  # Simple check if section exists
            issues.append({
                "type": "missing_reference",
                "reference": ref,
                "severity": "medium"
            })

    # 2. Check for placeholder markers
    if "[REVIEW NEEDED:" in contract_draft:
        review_items = re.findall(r'\[REVIEW NEEDED: ([^\]]+)\]', contract_draft)
        for item in review_items:
            issues.append({
                "type": "review_needed",
                "item": item,
                "severity": "high"
            })

    # 3. Check data consistency (party names)
    vp_data = state.get("verhandlungsprotokoll_data", {}) or {}
    if vp_data.get("contractor"):
        contractor_name = vp_data["contractor"].get("name", "")
        if contractor_name and contractor_name not in contract_draft:
            issues.append({
                "type": "missing_data",
                "field": "contractor_name",
                "severity": "high"
            })

    updates["consistency_issues"] = issues
    updates["messages"].append({
        "role": "system",
        "content": f"✓ Found {len(issues)} consistency issues"
    })

    return updates
```

---

### [8] Quality Reviewer

**Purpose**: Assess overall quality

```python
def quality_reviewer_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Review contract quality.
    """
    print("⭐ Reviewing quality...")

    updates = {
        "current_step": "quality_reviewer",
        "messages": []
    }

    contract_draft = state.get("contract_draft", "")
    consistency_issues = state.get("consistency_issues", [])
    outline = state.get("contract_outline", [])

    # Simple quality scoring
    quality_score = 100.0

    # Penalize for issues
    for issue in consistency_issues:
        if issue["severity"] == "high":
            quality_score -= 10
        elif issue["severity"] == "medium":
            quality_score -= 5

    # Penalize for short sections
    if len(contract_draft) < 1000:
        quality_score -= 20

    # Penalize for missing sections
    generated_sections = state.get("generated_sections", {})
    missing_sections = len(outline) - len(generated_sections)
    quality_score -= missing_sections * 15

    quality_score = max(0, min(100, quality_score))

    updates["quality_score"] = quality_score
    updates["quality_report"] = {
        "score": quality_score,
        "issues_count": len(consistency_issues),
        "sections_generated": len(generated_sections),
        "sections_required": len(outline),
        "contract_length": len(contract_draft)
    }

    updates["messages"].append({
        "role": "system",
        "content": f"✓ Quality score: {quality_score:.1f}/100"
    })

    return updates
```

---

### [9] Output Formatter

**Purpose**: Generate final files

```python
from docx import Document
import os
from datetime import datetime

def output_formatter_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Format and export contract.
    """
    print("📄 Formatting output...")

    updates = {
        "current_step": "output_formatter",
        "messages": [],
        "output_files": {}
    }

    contract_draft = state.get("contract_draft", "")
    contract_type_data = state.get("contract_type_data", {})
    quality_report = state.get("quality_report", {})

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "data/output"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Save text version
    txt_path = f"{output_dir}/contract_{timestamp}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"{contract_type_data.get('name')}\n")
        f.write("=" * 80 + "\n\n")
        f.write(contract_draft)

    updates["output_files"]["txt"] = txt_path

    # 2. Generate DOCX
    doc = Document()
    doc.add_heading(contract_type_data.get('name'), 0)
    doc.add_paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    doc.add_paragraph(f"Quality Score: {quality_report.get('score', 0):.1f}/100")
    doc.add_page_break()

    # Add contract text
    for paragraph in contract_draft.split('\n\n'):
        if paragraph.strip().startswith('§'):
            doc.add_heading(paragraph.strip(), level=1)
        else:
            doc.add_paragraph(paragraph.strip())

    docx_path = f"{output_dir}/contract_{timestamp}.docx"
    doc.save(docx_path)
    updates["output_files"]["docx"] = docx_path

    updates["messages"].append({
        "role": "system",
        "content": f"✓ Generated outputs:\n  - {txt_path}\n  - {docx_path}"
    })

    return updates
```

---

## Graph Construction

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

def create_contract_drafting_graph():
    """
    Create the contract drafting workflow.
    """
    graph = StateGraph(ContractDraftingState)

    # Add nodes
    graph.add_node("user_input_handler", user_input_handler_node)
    graph.add_node("document_extractor", document_extractor_node)  # Existing
    graph.add_node("excel_extractor", excel_extractor_node)  # Existing
    graph.add_node("knowledge_base_fetcher", knowledge_base_fetcher_node)
    graph.add_node("structure_analyzer", structure_analyzer_node)
    graph.add_node("content_mapper", content_mapper_node)
    graph.add_node("clause_generator", clause_generator_node)
    graph.add_node("consistency_checker", consistency_checker_node)
    graph.add_node("quality_reviewer", quality_reviewer_node)
    graph.add_node("output_formatter", output_formatter_node)

    # Define flow
    graph.add_edge(START, "user_input_handler")
    graph.add_edge("user_input_handler", "document_extractor")
    graph.add_edge("document_extractor", "excel_extractor")
    graph.add_edge("excel_extractor", "knowledge_base_fetcher")
    graph.add_edge("knowledge_base_fetcher", "structure_analyzer")
    graph.add_edge("structure_analyzer", "content_mapper")
    graph.add_edge("content_mapper", "clause_generator")
    graph.add_edge("clause_generator", "consistency_checker")
    graph.add_edge("consistency_checker", "quality_reviewer")
    graph.add_edge("quality_reviewer", "output_formatter")
    graph.add_edge("output_formatter", END)

    # Compile
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)
```

---

## Usage Example

```python
# Initialize state
initial_state = {
    "contract_type_id": "00827bca-eccf-4e5a-87bb-dcd438c4ff29",  # Site Supervision
    "project_description": "Construction site supervision for office building project in Berlin...",
    "uploaded_documents": [
        {"type": "verhandlungsprotokoll", "path": "data/vp.pdf"},
        {"type": "leistungsverzeichnis", "path": "data/lv.xlsx"}
    ]
}

# Run workflow
graph = create_contract_drafting_graph()
result = graph.invoke(initial_state, {"configurable": {"thread_id": "1"}})

# Access results
print(f"Quality Score: {result['quality_score']}")
print(f"Output Files: {result['output_files']}")
print(f"Contract Draft:\n{result['contract_draft'][:500]}...")
```

---

## Key Points

1. ✅ **No database changes** - Just read from existing Supabase tables
2. ✅ **All data in state** - Everything flows through LangGraph state
3. ✅ **Simple queries** - Basic SELECT queries to fetch data
4. ✅ **Reuse existing nodes** - Document and Excel extractors unchanged
5. ✅ **Contract types from JSON** - Load from `contract_types_rows.json`
6. ✅ **Modular** - Each node is independent and testable
7. ✅ **Graceful degradation** - KB fetch failure doesn't stop the workflow

## Graceful Degradation Strategy

The **Knowledge Base Fetcher** node is designed to fail gracefully:

### If Supabase Connection Fails:
- ✅ Returns empty arrays for `retrieved_contracts`, `retrieved_clauses`, `contract_structures`
- ✅ Logs warning message but doesn't throw error
- ✅ Workflow continues to next node
- ✅ Other nodes work without historical examples

### Impact of KB Failure:
- **Structure Analyzer**: Falls back to `required_sections` from contract type (no historical analysis)
- **Clause Generator**: Generates clauses without reference examples (pure LLM generation)
- **Quality**: May be slightly lower without examples, but still functional

### Why This Works:
```python
# Structure Analyzer handles missing KB data
retrieved_structures = state.get("contract_structures", [])
if retrieved_structures:
    # Use historical structures for analysis
    prompt += f"Historical Structures: {structures}"
else:
    # Fallback to contract type requirements only
    prompt += "No historical data - use required_sections only"

# Clause Generator handles missing examples
relevant_clauses = state.get("retrieved_clauses", [])
if relevant_clauses:
    prompt += f"Reference Examples: {clauses}"
else:
    prompt += "Generate from scratch using German legal standards"
```

The system **always works**, just with varying quality based on available data

---

This architecture is ready to implement! All nodes work with state data, no schema changes needed.
