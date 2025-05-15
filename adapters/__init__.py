"""
Adapters for different model providers.
"""

from .select_model import LiteLLMAdapter, set_default_adapter

__all__ = ['LiteLLMAdapter', 'set_default_adapter']
