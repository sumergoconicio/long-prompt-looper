"""
Core Module Exports for Prompt Chaining System

Description: Exposes all core processing functions for main.py, avoiding module/function confusion.
Author: ChAI-Engine (chaiji)
Last Updated: 2025-05-15
Non-standard deps: None (standard library only)
Abstract Spec: Exports get_user_inputs, combine_prompts, query_model, save_response for direct import in main.py.
Design Rationale: Ensures that main.py imports functions, not modules, to prevent 'module' object is not callable errors.
"""

from .get_inputs import get_user_inputs
from .prompt_combiner import combine_prompts
from .query_model import query_model
from .save_response import save_response

__all__ = ['get_user_inputs', 'combine_prompts', 'query_model', 'save_response']
