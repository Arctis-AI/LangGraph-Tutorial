# LangSmith Quick Start Guide

Get your Contract Draft POC app deployed and monitored on LangSmith in 5 minutes.

## What is LangSmith?

LangSmith is a platform for:
- **Monitoring** LangChain/LangGraph applications
- **Debugging** LLM calls and workflow execution
- **Evaluating** performance and quality
- **Deploying** LangGraph apps (via LangGraph Cloud)

## Option 1: Enable Tracing Only (Fastest)

Just want to monitor your local app? Follow these steps:

### 1. Get Your API Key

Visit [smith.langchain.com/settings](https://smith.langchain.com/settings) and create an API key.

### 2. Update `.env`

Add these lines to your `.env` file:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_your_api_key_here
LANGCHAIN_PROJECT=contract-draft-poc
```

### 3. Run Your App

```bash
uv run python main.py
```

### 4. View Traces

Go to [smith.langchain.com](https://smith.langchain.com/) → Select your project **contract-draft-poc** → View traces!

**That's it!** Your app is now sending traces to LangSmith.

---

## Option 2: Deploy to LangGraph Cloud (Full Hosting)

Want to deploy your app as an API? Follow these steps:

### 1. Install LangGraph CLI

```bash
uv add langgraph-cli
```

### 2. Test Locally First

```bash
# Start local server
langgraph up

# In another terminal, test the API
curl http://localhost:8123/assistants
```

### 3. Login to LangSmith

```bash
langgraph login
```

Follow the prompts to authenticate.

### 4. Deploy

```bash
langgraph deploy
```

You'll be asked:
- **Organization**: Choose your org
- **Deployment name**: e.g., `contract-draft-prod`
- **Environment variables**: Set your API keys

### 5. Use Your Deployed API

After deployment, you'll get an endpoint like:

```
https://contract-draft-prod-abc123.us.langgraph.app
```

Test it:

```bash
curl -X POST https://your-deployment.langgraph.app/runs/stream \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"assistant_id": "contract_generator", "input": {...}}'
```

---

## What You'll See in LangSmith

### Traces Tab
- Complete workflow execution timeline
- Each node (upload_handler → document_extractor → etc.)
- Duration and status of each step

### LLM Calls
- Every call to Anthropic Claude
- Full prompt and response
- Token usage and cost
- Latency metrics

### Feedback & Evaluation
- Quality scores from quality_checker node
- Validation errors
- Custom metrics

### Monitoring
- Success/failure rates
- Average execution time
- Token consumption trends
- Cost per contract generated

---

## Example: What a Trace Looks Like

```
Run: contract_generation_001
├── upload_handler (0.1s) ✓
│   └── Files: VP.docx, LV.xlsx
├── document_classifier (0.05s) ✓
│   └── Status: both_documents
├── document_extractor (12.3s) ✓
│   ├── LLM Call: claude-sonnet-4
│   │   ├── Tokens: 8,234 in / 1,456 out
│   │   ├── Cost: $0.12
│   │   └── Latency: 11.8s
│   └── Extracted: Project, Parties, Terms
├── excel_extractor (0.8s) ✓
│   └── Items: 15 performance items
├── data_validator (0.2s) ✓
│   └── Validation: PASSED
├── data_merger (0.1s) ✓
├── contract_generator (0.5s) ✓
│   └── Generated: 8,234 characters
├── quality_checker (0.1s) ✓
│   └── Score: 88.9%
└── output_formatter (0.3s) ✓
    └── Output: contract_20251125.docx

Total Duration: 14.5s
Total Cost: $0.12
Status: SUCCESS
```

---

## Tips for Effective Monitoring

### 1. Use Descriptive Project Names

```bash
# Development
LANGCHAIN_PROJECT=contract-draft-dev

# Production
LANGCHAIN_PROJECT=contract-draft-prod
```

### 2. Add Custom Metadata

You can add metadata to traces:

```python
from langsmith import traceable

@traceable(metadata={"doc_type": "VP", "language": "de"})
def extract_data(doc):
    # Your extraction logic
    pass
```

### 3. Set Up Alerts

In LangSmith dashboard:
1. Go to **Settings** → **Alerts**
2. Create alert for:
   - Failed runs
   - High latency (>30s)
   - High cost (>$1 per run)

### 4. Use Tags

Tag your runs for easier filtering:

```python
from langchain_core.tracers import LangChainTracer

tracer = LangChainTracer(tags=["production", "german", "version-2.0"])
```

---

## Troubleshooting

### Traces Not Appearing

**Check:**
1. `LANGCHAIN_TRACING_V2=true` is set
2. API key is valid (check [settings](https://smith.langchain.com/settings))
3. Project name doesn't have typos
4. You have internet connection
5. No firewall blocking `api.smith.langchain.com`

**Test connection:**
```bash
curl -H "x-api-key: $LANGCHAIN_API_KEY" https://api.smith.langchain.com/info
```

### Deployment Failed

**Common issues:**
- Missing dependencies in `requirements.txt`
- Wrong Python version (we use 3.12)
- Environment variables not set
- Network connectivity

**Check logs:**
```bash
langgraph logs --deployment-name contract-draft-prod
```

### High Costs

If costs are too high:
1. Use cheaper models: `claude-3-haiku` instead of `claude-sonnet-4`
2. Reduce max_tokens in prompts
3. Cache repeated extractions
4. Set budget alerts in LangSmith

---

## Next Steps

1. **Enable tracing** for your local development
2. **Review traces** after each run to understand flow
3. **Set up alerts** for production monitoring
4. **Deploy to Cloud** when ready for production
5. **Share dashboard** with your team

---

## Resources

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangGraph Cloud Docs](https://langchain-ai.github.io/langgraph/cloud/)
- [LangSmith Pricing](https://www.langchain.com/pricing)
- [API Reference](https://docs.smith.langchain.com/api)

---

## Quick Command Reference

```bash
# Enable tracing locally
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your-key
uv run python main.py

# Start local LangGraph server
langgraph up

# Deploy to cloud
langgraph login
langgraph deploy

# View deployment logs
langgraph logs

# List deployments
langgraph deployments list

# Update deployment
langgraph deploy --revision-id abc123
```

Happy monitoring! 🚀
