"""
Module for handling model queries.
"""
from typing import Optional, Dict, Any
import os
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# This will be set by the adapter
model_adapter = None

def set_model_adapter(adapter):
    """Set the model adapter to be used for queries.
    
    Args:
        adapter: The model adapter instance to use
    """
    global model_adapter
    model_adapter = adapter
    logger.info("Model adapter set successfully")

def query_model(prompt: str, **kwargs) -> str:
    """
    Query the model with the given prompt.
    
    Args:
        prompt: The prompt to send to the model
        **kwargs: Additional arguments to pass to the model adapter
        
    Returns:
        str: The model's response
        
    Raises:
        RuntimeError: If no model adapter is set
        Exception: For any errors during model query
    """
    if model_adapter is None:
        error_msg = "No model adapter set. Call set_model_adapter() first."
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    try:
        logger.info("Sending query to model...")
        response = model_adapter.query(prompt, **kwargs)
        logger.info("Received response from model")
        return response
    except Exception as e:
        logger.error(f"Error querying model: {str(e)}")
        raise

# Example adapter interface that concrete adapters should implement
class BaseModelAdapter:
    """Base class for model adapters."""
    
    def query(self, prompt: str, **kwargs) -> str:
        """
        Query the model with the given prompt.
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional arguments for the model
            
        Returns:
            str: The model's response
        """
        raise NotImplementedError("Subclasses must implement this method")
