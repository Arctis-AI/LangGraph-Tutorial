# Deployment Guide - Contract Draft POC

This guide covers multiple deployment options for the Contract Generation System.

## Table of Contents
1. [LangSmith Tracing (Monitoring)](#1-langsmith-tracing-monitoring)
2. [LangGraph Cloud Deployment](#2-langgraph-cloud-deployment)
3. [Docker Deployment](#3-docker-deployment)
4. [Local Development](#4-local-development)

---

## 1. LangSmith Tracing (Monitoring)

LangSmith provides observability for your LangChain/LangGraph applications. It tracks execution, logs, performance, and helps debug issues.

### Setup Steps

#### Step 1: Get LangSmith API Key

1. Go to [LangSmith](https://smith.langchain.com/)
2. Sign up or log in
3. Navigate to **Settings** → **API Keys**
4. Create a new API key

#### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
# Enable LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls_your-api-key-here
LANGCHAIN_PROJECT=contract-draft-poc
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

#### Step 3: Run Your Application

```bash
uv run python main.py
```

#### Step 4: View Traces

1. Go to [LangSmith Dashboard](https://smith.langchain.com/)
2. Select your project: **contract-draft-poc**
3. View traces, logs, and performance metrics

### What You'll See in LangSmith

- **Traces**: Complete execution flow of your contract generation
- **LLM Calls**: Every API call to Anthropic/OpenAI with inputs/outputs
- **Performance**: Latency, token usage, costs
- **Errors**: Stack traces and error details
- **Custom Metadata**: Document processing steps, validation results

---

## 2. LangGraph Cloud Deployment

LangGraph Cloud hosts your LangGraph application as an API service with built-in monitoring, streaming, and state management.

### Prerequisites

```bash
# Install LangGraph CLI
uv add langgraph-cli

# Or with pip
pip install langgraph-cli
```

### Deployment Steps

#### Step 1: Configure `langgraph.json`

Already created! The file specifies:
- Graph entry point: `src/contract_graph.py:create_contract_graph_with_routing`
- Python version: 3.12
- Environment file: `.env`

#### Step 2: Test Locally with LangGraph Server

```bash
# Start local LangGraph server
langgraph up

# Server runs at http://localhost:8123
```

#### Step 3: Test the API

```bash
# Test with curl
curl -X POST http://localhost:8123/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "contract_generator",
    "input": {
      "messages": [],
      "uploaded_files": {},
      "validation_errors": [],
      "validation_passed": false,
      "quality_passed": false,
      "retry_count": 0,
      "processing_status": "starting",
      "current_step": "init"
    },
    "config": {
      "configurable": {
        "thread_id": "test-001"
      }
    }
  }'
```

#### Step 4: Deploy to LangGraph Cloud

```bash
# Login to LangSmith
langgraph login

# Deploy your graph
langgraph deploy

# Follow the prompts to:
# - Select organization
# - Set deployment name
# - Configure environment variables
```

#### Step 5: Access Your Deployed API

After deployment, you'll get:
- **API Endpoint**: `https://your-deployment.langgraph.cloud`
- **API Key**: For authentication
- **Dashboard**: Monitor and manage your deployment

### API Usage Example

```python
import requests

API_URL = "https://your-deployment.langgraph.cloud"
API_KEY = "your-api-key"

response = requests.post(
    f"{API_URL}/runs/stream",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "assistant_id": "contract_generator",
        "input": {
            "messages": [],
            "processing_status": "starting"
        },
        "config": {
            "configurable": {"thread_id": "unique-id"}
        }
    },
    stream=True
)

for chunk in response.iter_lines():
    print(chunk.decode())
```

---

## 3. Docker Deployment

Deploy as a containerized application for flexibility and portability.

### Build Docker Image

```bash
# Build the image
docker build -t contract-draft-poc .

# Run the container
docker run -it --rm \
  -v $(pwd)/resource:/app/resource \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  contract-draft-poc
```

### Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  contract-generator:
    build: .
    volumes:
      - ./resource:/app/resource
      - ./data:/app/data
    env_file:
      - .env
    ports:
      - "8000:8000"
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

---

## 4. Local Development

### Quick Start

```bash
# Clone and navigate to the project
cd contract-draft-poc

# Install dependencies with uv
uv sync

# Copy .env.example to .env and configure
cp .env.example .env
# Edit .env with your API keys

# Run the application
uv run python main.py
```

### Development with LangSmith Tracing

```bash
# Enable tracing in .env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-key

# Run and monitor in LangSmith
uv run python main.py
```

---

## Environment Variables Reference

### Required

```bash
# LLM Provider (choose one)
DEFAULT_LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

### Optional - OpenAI

```bash
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4-turbo
```

### Optional - Azure OpenAI

```bash
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=...
```

### Optional - LangSmith

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls_...
LANGCHAIN_PROJECT=contract-draft-poc
```

---

## Troubleshooting

### LangSmith Not Receiving Traces

**Issue**: Traces not appearing in LangSmith dashboard

**Solutions**:
1. Verify `LANGCHAIN_TRACING_V2=true` is set
2. Check API key is valid
3. Ensure project name matches
4. Check internet connectivity
5. Look for errors in console output

### LangGraph Cloud Deployment Fails

**Issue**: `langgraph deploy` fails

**Solutions**:
1. Check `langgraph.json` syntax
2. Verify all dependencies in `requirements.txt`
3. Ensure Python version compatibility (3.12)
4. Check environment variables are set correctly
5. Review deployment logs: `langgraph logs`

### Docker Container Crashes

**Issue**: Container exits immediately

**Solutions**:
1. Check `.env` file is properly mounted
2. Verify all required API keys are set
3. Check resource folder has proper permissions
4. Review logs: `docker logs <container-id>`

---

## Production Considerations

### Security

- **Never commit** `.env` files to version control
- Use **secrets management** (AWS Secrets Manager, Vault, etc.)
- Enable **API authentication** for deployed services
- Use **HTTPS** for all external communications

### Monitoring

- Enable **LangSmith tracing** for all environments
- Set up **alerts** for failures or performance issues
- Monitor **token usage** and costs
- Track **quality metrics** (validation pass rate, etc.)

### Scaling

- Use **LangGraph Cloud** for automatic scaling
- Implement **rate limiting** to prevent abuse
- Consider **async processing** for large batches
- Use **Redis/PostgreSQL** for persistent state management

### Cost Optimization

- Choose appropriate **model sizes** (Claude Sonnet vs Opus)
- Implement **caching** for repeated extractions
- Monitor **token usage** via LangSmith
- Set **budget alerts** in LangSmith

---

## Support

For issues or questions:
1. Check [LangSmith Documentation](https://docs.smith.langchain.com/)
2. Review [LangGraph Cloud Docs](https://langchain-ai.github.io/langgraph/cloud/)
3. Open an issue in the project repository

---

## Quick Reference Commands

```bash
# Local development
uv run python main.py

# Test with LangSmith tracing
LANGCHAIN_TRACING_V2=true uv run python main.py

# Start LangGraph server locally
langgraph up

# Deploy to LangGraph Cloud
langgraph deploy

# Build and run Docker
docker build -t contract-draft-poc . && docker run -it --rm --env-file .env contract-draft-poc

# Docker Compose
docker-compose up -d
```
