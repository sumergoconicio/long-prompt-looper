"""
Model adapter implementation using LiteLLM.
"""
import os
import logging
from typing import Dict, Any, Optional

# Import the base model interface from core
from core.query_model import BaseModelAdapter

# Set up logging
logger = logging.getLogger(__name__)

# Default model parameters
DEFAULT_PARAMS = {
    'temperature': 0.7,
    'max_tokens': 32768,
    'top_p': 1.0,
    'frequency_penalty': 0.0,
    'presence_penalty': 0.0,
}

class LiteLLMAdapter(BaseModelAdapter):
    """Adapter for LiteLLM API."""
    
    def __init__(self, model_name: str = "gpt-4.1", **model_params):
        """Initialize the LiteLLM adapter.
        
        Args:
            model_name: Name of the model to use (e.g., 'gpt-3.5-turbo')
            **model_params: Additional model parameters
        """
        self.model_name = model_name
        self.model_params = {**DEFAULT_PARAMS, **model_params}
        self._validate_environment()
    
    def _validate_environment(self) -> None:
        """Validate that required environment variables are set."""
        required_vars = ['OPENAI_API_KEY']  # Add other required vars as needed
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
    
    def query(self, prompt: str, **kwargs) -> str:
        """
        Query the model with the given prompt.
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional parameters to override defaults
            
        Returns:
            str: The model's response
            
        Raises:
            Exception: If there's an error querying the model
        """
        try:
            import litellm
            
            # Merge default params with any overrides
            params = {**self.model_params, **kwargs}
            
            logger.info(f"Sending request to {self.model_name}...")
            response = litellm.completion(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                **params
            )
            
            # Extract the response content
            content = response.choices[0].message.content
            logger.info(f"Received response from {self.model_name}")
            
            return content
            
        except ImportError:
            error_msg = "LiteLLM not installed. Please install with: pip install litellm"
            logger.error(error_msg)
            raise ImportError(error_msg)
        except Exception as e:
            error_msg = f"Error querying {self.model_name}: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) from e

def set_default_adapter(model_name: str = "gpt-4.1", **model_params) -> LiteLLMAdapter:
    """
    Create and set the default model adapter.
    
    Args:
        model_name: Name of the model to use
        **model_params: Additional model parameters
        
    Returns:
        LiteLLMAdapter: The created adapter instance
    """
    adapter = LiteLLMAdapter(model_name, **model_params)
    from core.query_model import set_model_adapter
    set_model_adapter(adapter)
    return adapter
