# LLM Client Manager

This module provides a unified interface for working with multiple LLM providers in the contract draft application.

## Supported Providers

- **Anthropic (Claude)**: Claude Sonnet 4 and other models
- **OpenAI**: GPT-4, GPT-4-turbo, and other models
- **Azure OpenAI**: Enterprise deployments of OpenAI models

## Quick Start

### Basic Usage

```python
from src.core.llm_clients import get_llm_client

# Use default provider from config
llm = get_llm_client()
response = llm.invoke([
    {"role": "user", "content": "Extract data from this document..."}
])
```

### Specify a Provider

```python
# Use Anthropic Claude
llm = get_llm_client(provider="anthropic")

# Use OpenAI GPT-4
llm = get_llm_client(provider="openai", model="gpt-4-turbo")

# Use Azure OpenAI
llm = get_llm_client(provider="azure")
```

### Custom Parameters

```python
# Use custom temperature and max tokens
llm = get_llm_client(
    provider="anthropic",
    model="claude-sonnet-4-20250514",
    temperature=0.5,
    max_tokens=4000
)
```

## Configuration

Set up your provider credentials in `.env`:

```bash
# Required: Choose your default provider
DEFAULT_LLM_PROVIDER=anthropic

# Anthropic
ANTHROPIC_API_KEY=your-key-here
ANTHROPIC_DEFAULT_MODEL=claude-sonnet-4-20250514

# OpenAI (optional)
OPENAI_API_KEY=your-key-here
OPENAI_DEFAULT_MODEL=gpt-4-turbo

# Azure OpenAI (optional)
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
```

## Utility Functions

### Get Available Providers

```python
from src.core.llm_clients import get_available_providers

providers = get_available_providers()
print(f"Configured providers: {providers}")
# Output: ['anthropic', 'openai']
```

### Validate Provider Configuration

```python
from src.core.llm_clients import validate_provider_config

is_valid, error_msg = validate_provider_config("anthropic")
if not is_valid:
    print(f"Configuration error: {error_msg}")
```

## Switching Providers

You can easily switch between providers by:

1. **Environment Variable**: Change `DEFAULT_LLM_PROVIDER` in `.env`
2. **Code**: Pass `provider` parameter to `get_llm_client()`
3. **Runtime**: Update `config.DEFAULT_LLM_PROVIDER` dynamically

Example of runtime switching:

```python
import config
from src.core.llm_clients import get_llm_client

# Try Anthropic first
try:
    llm = get_llm_client(provider="anthropic")
except ValueError:
    # Fall back to OpenAI
    llm = get_llm_client(provider="openai")
```

## Provider-Specific Models

### Anthropic Models
- `claude-sonnet-4-20250514` (default)
- `claude-opus-4-20250514`
- `claude-3-5-sonnet-20241022`

### OpenAI Models
- `gpt-4-turbo` (default)
- `gpt-4`
- `gpt-3.5-turbo`

### Azure OpenAI
Uses deployment names configured in your Azure portal.

## Error Handling

The client manager provides clear error messages:

```python
try:
    llm = get_llm_client(provider="anthropic")
except ValueError as e:
    print(f"Provider error: {e}")
    # Output: "ANTHROPIC_API_KEY not set in environment variables."
```

## Best Practices

1. **Use defaults**: Call `get_llm_client()` without parameters for most use cases
2. **Configure once**: Set up `.env` file and forget about provider details
3. **Error handling**: Always wrap provider initialization in try-except
4. **Cost awareness**: Different providers have different pricing - choose accordingly
5. **Model selection**: Use faster models (e.g., GPT-3.5) for simple tasks

## Architecture

The module uses a factory pattern with:
- `LLMClientManager`: Main class managing provider instances
- `get_llm_client()`: Convenience function for quick access
- Provider-specific methods: `_create_anthropic_client()`, etc.
- Configuration validation: Checks credentials before creating clients

## Integration with Existing Code

All nodes in the application should use this client manager:

```python
# OLD WAY (deprecated)
from langchain.chat_models import init_chat_model
llm = init_chat_model("anthropic:claude-sonnet-4-20250514")

# NEW WAY (recommended)
from src.core.llm_clients import get_llm_client
llm = get_llm_client()  # Uses configured defaults
```

## Troubleshooting

### "No LLM provider configured" error
- Make sure at least one provider's credentials are set in `.env`
- Check that `.env` file is in the project root
- Verify credentials are valid (no typos, proper format)

### "DEFAULT_LLM_PROVIDER not configured" error
- Set `DEFAULT_LLM_PROVIDER` in `.env` to match your configured provider
- Valid options: "anthropic", "openai", "azure"

### Module import errors
- Install required packages: `pip install langchain-anthropic langchain-openai`
- Ensure virtual environment is activated
