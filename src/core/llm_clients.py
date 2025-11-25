"""
LLM Client Manager with support for multiple providers.

Supports:
- Anthropic (Claude)
- OpenAI (GPT models)
- Azure OpenAI

Usage:
    from src.core.llm_clients import get_llm_client

    # Get client using default provider from config
    llm = get_llm_client()

    # Or specify a provider explicitly
    llm = get_llm_client(provider="anthropic")
    llm = get_llm_client(provider="openai", model="gpt-4")
    llm = get_llm_client(provider="azure")
"""

from typing import Optional, Literal
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI, AzureChatOpenAI
import config


# Type alias for supported providers
ProviderType = Literal["anthropic", "openai", "azure"]


class LLMClientManager:
    """Manager class for LLM clients with provider switching capabilities."""

    def __init__(self):
        """Initialize the LLM client manager."""
        self.default_provider = config.DEFAULT_LLM_PROVIDER
        self.default_model = config.DEFAULT_LLM_MODEL

    def get_client(
        self,
        provider: Optional[ProviderType] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """
        Get an LLM client instance.

        Args:
            provider: The provider to use ("anthropic", "openai", "azure").
                     If None, uses the default from config.
            model: The specific model to use. If None, uses the default for the provider.
            temperature: Temperature setting for the model (0.0 to 1.0).
            max_tokens: Maximum tokens for the response.
            **kwargs: Additional provider-specific arguments.

        Returns:
            A LangChain chat model instance.

        Examples:
            # Use default provider and model
            llm = manager.get_client()

            # Specify Anthropic with custom model
            llm = manager.get_client(provider="anthropic", model="claude-sonnet-4-20250514")

            # Use OpenAI with GPT-4
            llm = manager.get_client(provider="openai", model="gpt-4-turbo")

            # Use Azure OpenAI
            llm = manager.get_client(provider="azure")
        """
        # Use default provider if not specified
        if provider is None:
            provider = self.default_provider

        # Use default model if not specified
        if model is None:
            model = self._get_default_model(provider)

        # Route to appropriate client creation method
        if provider == "anthropic":
            return self._create_anthropic_client(model, temperature, max_tokens, **kwargs)
        elif provider == "openai":
            return self._create_openai_client(model, temperature, max_tokens, **kwargs)
        elif provider == "azure":
            return self._create_azure_client(model, temperature, max_tokens, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'anthropic', 'openai', or 'azure'.")

    def _get_default_model(self, provider: ProviderType) -> str:
        """Get the default model for a given provider."""
        if provider == "anthropic":
            return config.ANTHROPIC_DEFAULT_MODEL
        elif provider == "openai":
            return config.OPENAI_DEFAULT_MODEL
        elif provider == "azure":
            return config.AZURE_OPENAI_DEPLOYMENT_NAME
        return self.default_model

    def _create_anthropic_client(
        self,
        model: str,
        temperature: float,
        max_tokens: Optional[int],
        **kwargs
    ) -> ChatAnthropic:
        """Create an Anthropic (Claude) client."""
        api_key = config.ANTHROPIC_API_KEY
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment variables.")

        client_kwargs = {
            "model": model,
            "anthropic_api_key": api_key,
            "temperature": temperature,
        }

        if max_tokens:
            client_kwargs["max_tokens"] = max_tokens

        # Add any additional kwargs
        client_kwargs.update(kwargs)

        return ChatAnthropic(**client_kwargs)

    def _create_openai_client(
        self,
        model: str,
        temperature: float,
        max_tokens: Optional[int],
        **kwargs
    ) -> ChatOpenAI:
        """Create an OpenAI client."""
        api_key = config.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment variables.")

        client_kwargs = {
            "model": model,
            "openai_api_key": api_key,
            "temperature": temperature,
        }

        if max_tokens:
            client_kwargs["max_tokens"] = max_tokens

        # Add any additional kwargs
        client_kwargs.update(kwargs)

        return ChatOpenAI(**client_kwargs)

    def _create_azure_client(
        self,
        model: str,
        temperature: float,
        max_tokens: Optional[int],
        **kwargs
    ) -> AzureChatOpenAI:
        """Create an Azure OpenAI client."""
        api_key = config.AZURE_OPENAI_API_KEY
        endpoint = config.AZURE_OPENAI_ENDPOINT
        api_version = config.AZURE_OPENAI_API_VERSION
        deployment_name = model  # In Azure, the model is the deployment name

        if not all([api_key, endpoint, api_version, deployment_name]):
            raise ValueError(
                "Azure OpenAI requires AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, "
                "AZURE_OPENAI_API_VERSION, and AZURE_OPENAI_DEPLOYMENT_NAME to be set."
            )

        client_kwargs = {
            "azure_deployment": deployment_name,
            "openai_api_version": api_version,
            "azure_endpoint": endpoint,
            "api_key": api_key,
            "temperature": temperature,
        }

        if max_tokens:
            client_kwargs["max_tokens"] = max_tokens

        # Add any additional kwargs
        client_kwargs.update(kwargs)

        return AzureChatOpenAI(**client_kwargs)


# Global instance for convenience
_manager = LLMClientManager()


def get_llm_client(
    provider: Optional[ProviderType] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    **kwargs
):
    """
    Convenience function to get an LLM client.

    This is the main function you should use to get LLM clients throughout the application.

    Args:
        provider: The provider to use ("anthropic", "openai", "azure").
                 If None, uses the default from config.
        model: The specific model to use. If None, uses the default for the provider.
        temperature: Temperature setting for the model (0.0 to 1.0).
        max_tokens: Maximum tokens for the response.
        **kwargs: Additional provider-specific arguments.

    Returns:
        A LangChain chat model instance.

    Examples:
        # Use default provider and model
        llm = get_llm_client()
        response = llm.invoke([{"role": "user", "content": "Hello!"}])

        # Use Anthropic Claude
        llm = get_llm_client(provider="anthropic", model="claude-sonnet-4-20250514")

        # Use OpenAI GPT-4
        llm = get_llm_client(provider="openai", model="gpt-4-turbo")

        # Use Azure OpenAI with custom settings
        llm = get_llm_client(provider="azure", temperature=0.5, max_tokens=2000)
    """
    return _manager.get_client(provider, model, temperature, max_tokens, **kwargs)


def get_available_providers() -> list[str]:
    """
    Get a list of available providers based on configured credentials.

    Returns:
        List of provider names that have credentials configured.
    """
    available = []

    # Check Anthropic
    if config.ANTHROPIC_API_KEY:
        available.append("anthropic")

    # Check OpenAI
    if config.OPENAI_API_KEY:
        available.append("openai")

    # Check Azure OpenAI
    if all([
        config.AZURE_OPENAI_API_KEY,
        config.AZURE_OPENAI_ENDPOINT,
        config.AZURE_OPENAI_API_VERSION,
        config.AZURE_OPENAI_DEPLOYMENT_NAME
    ]):
        available.append("azure")

    return available


def validate_provider_config(provider: ProviderType) -> tuple[bool, Optional[str]]:
    """
    Validate that a provider has all required configuration.

    Args:
        provider: The provider to validate.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if provider == "anthropic":
        if not config.ANTHROPIC_API_KEY:
            return False, "ANTHROPIC_API_KEY not set in environment variables"
        return True, None

    elif provider == "openai":
        if not config.OPENAI_API_KEY:
            return False, "OPENAI_API_KEY not set in environment variables"
        return True, None

    elif provider == "azure":
        missing = []
        if not config.AZURE_OPENAI_API_KEY:
            missing.append("AZURE_OPENAI_API_KEY")
        if not config.AZURE_OPENAI_ENDPOINT:
            missing.append("AZURE_OPENAI_ENDPOINT")
        if not config.AZURE_OPENAI_API_VERSION:
            missing.append("AZURE_OPENAI_API_VERSION")
        if not config.AZURE_OPENAI_DEPLOYMENT_NAME:
            missing.append("AZURE_OPENAI_DEPLOYMENT_NAME")

        if missing:
            return False, f"Missing Azure configuration: {', '.join(missing)}"
        return True, None

    else:
        return False, f"Unknown provider: {provider}"
