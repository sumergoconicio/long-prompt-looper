"""
Module for saving model responses to files.
"""
import os
import logging
from pathlib import Path
from typing import Optional

# Initialize logger
logger = logging.getLogger(__name__)

def ensure_output_dir(output_dir: str) -> None:
    """Ensure the output directory exists.
    
    Args:
        output_dir: Path to the output directory
    """
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured output directory exists: {output_dir}")
    except Exception as e:
        logger.error(f"Error creating output directory {output_dir}: {str(e)}")
        raise

def generate_output_filename(
    output_dir: str,
    var_a_name: str,
    var_b_name: str,
    extension: str = "txt"
) -> str:
    """Generate a standardized output filename.
    
    Args:
        output_dir: Base output directory
        var_a_name: Name of Variable A file (without extension)
        var_b_name: Name of Variable B file (without extension)
        extension: File extension to use (without dot)
        
    Returns:
        str: Full path to the output file
    """
    # Clean and sanitize filenames
    def sanitize(name: str) -> str:
        return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)
    
    safe_var_a = sanitize(var_a_name)
    safe_var_b = sanitize(var_b_name)
    
    # Remove 'NONE' parts and create appropriate filename
    parts = []
    if safe_var_a != 'NONE':
        parts.append(safe_var_a)
    if safe_var_b != 'NONE':
        parts.append(safe_var_b)
    
    if not parts:
        filename = f"response.{extension}"
    else:
        filename = f"{'-'.join(parts)}-response.{extension}"
    return os.path.join(output_dir, filename)

def save_response(
    content: str,
    output_dir: str,
    var_a_name: str,
    var_b_name: str,
    extension: str = "txt"
) -> str:
    """Save the model response to a file.
    
    Args:
        content: The content to save
        output_dir: Directory to save the file in
        var_a_name: Name of Variable A file (without extension)
        var_b_name: Name of Variable B file (without extension)
        extension: File extension to use (without dot)
        
    Returns:
        str: Path to the saved file
        
    Raises:
        IOError: If there's an error writing the file
    """
    try:
        ensure_output_dir(output_dir)
        output_path = generate_output_filename(output_dir, var_a_name, var_b_name, extension)
        
        # Ensure we don't overwrite existing files
        counter = 1
        base_path = output_path
        while os.path.exists(output_path):
            name, ext = os.path.splitext(base_path)
            output_path = f"{name}_{counter}{ext}"
            counter += 1
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Saved response to {output_path}")
        return output_path
        
    except Exception as e:
        error_msg = f"Error saving response to file: {str(e)}"
        logger.error(error_msg)
        raise IOError(error_msg) from e
