# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== LLM Provider Configuration ====================

# Default LLM Provider: "anthropic", "openai", or "azure"
DEFAULT_LLM_PROVIDER = os.getenv('DEFAULT_LLM_PROVIDER', 'anthropic')

# Default model for each provider (can be overridden via environment variables)
DEFAULT_LLM_MODEL = os.getenv('DEFAULT_LLM_MODEL', 'claude-sonnet-4-20250514')

# ==================== Anthropic Configuration ====================
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
ANTHROPIC_DEFAULT_MODEL = os.getenv('ANTHROPIC_DEFAULT_MODEL', 'claude-sonnet-4-20250514')

# ==================== OpenAI Configuration ====================
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_DEFAULT_MODEL = os.getenv('OPENAI_DEFAULT_MODEL', 'gpt-4-turbo')

# ==================== Azure OpenAI Configuration ====================
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')

# ==================== LangSmith Configuration ====================
# Enable LangSmith tracing for monitoring and debugging
LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2', 'false').lower() == 'true'
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
LANGCHAIN_PROJECT = os.getenv('LANGCHAIN_PROJECT', 'contract-draft-poc')
LANGCHAIN_ENDPOINT = os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')


def validate_config():
    """
    Validates that at least one LLM provider is configured.
    Raises ValueError if no provider credentials are found.
    """
    has_anthropic = bool(ANTHROPIC_API_KEY)
    has_openai = bool(OPENAI_API_KEY)
    has_azure = all([
        AZURE_OPENAI_API_KEY,
        AZURE_OPENAI_ENDPOINT,
        AZURE_OPENAI_API_VERSION,
        AZURE_OPENAI_DEPLOYMENT_NAME
    ])

    if not (has_anthropic or has_openai or has_azure):
        raise ValueError(
            "No LLM provider configured. Please set credentials for at least one provider:\n"
            "- Anthropic: ANTHROPIC_API_KEY\n"
            "- OpenAI: OPENAI_API_KEY\n"
            "- Azure: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, "
            "AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_NAME"
        )

    # Validate that the default provider is actually configured
    if DEFAULT_LLM_PROVIDER == 'anthropic' and not has_anthropic:
        raise ValueError(
            f"DEFAULT_LLM_PROVIDER is set to '{DEFAULT_LLM_PROVIDER}' but "
            "ANTHROPIC_API_KEY is not configured."
        )
    elif DEFAULT_LLM_PROVIDER == 'openai' and not has_openai:
        raise ValueError(
            f"DEFAULT_LLM_PROVIDER is set to '{DEFAULT_LLM_PROVIDER}' but "
            "OPENAI_API_KEY is not configured."
        )
    elif DEFAULT_LLM_PROVIDER == 'azure' and not has_azure:
        raise ValueError(
            f"DEFAULT_LLM_PROVIDER is set to '{DEFAULT_LLM_PROVIDER}' but "
            "Azure OpenAI credentials are not fully configured."
        )

    # Print available providers for debugging
    available_providers = []
    if has_anthropic:
        available_providers.append("anthropic")
    if has_openai:
        available_providers.append("openai")
    if has_azure:
        available_providers.append("azure")

    print(f"✓ Configured LLM providers: {', '.join(available_providers)}")
    print(f"✓ Default provider: {DEFAULT_LLM_PROVIDER}")


validate_config()