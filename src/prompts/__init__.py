"""Prompts module for contract draft generation."""

from .document_extraction import DOCUMENT_EXTRACTION_PROMPT, FIELD_EXTRACTION_PROMPT_TEMPLATE

__all__ = [
    "DOCUMENT_EXTRACTION_PROMPT",
    "FIELD_EXTRACTION_PROMPT_TEMPLATE",
]