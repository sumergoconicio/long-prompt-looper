"""
Module for combining different prompt components into a single prompt.
"""
from typing import Dict, Tuple
import os

def read_file_content(file_path: str) -> str:
    """Read content from a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        str: File contents
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def extract_filename(file_path: str) -> str:
    """Extract just the filename without extension from a path.
    
    Args:
        file_path: Full path to the file
        
    Returns:
        str: Filename without extension
    """
    base = os.path.basename(file_path)
    return os.path.splitext(base)[0]

def combine_prompts(
    system_prompt_path: str,
    var_a_path: str,
    var_b_path: str,
    task_prompt_path: str
) -> Tuple[str, str, str]:
    """Combine all prompt components into a single prompt.
    
    Args:
        system_prompt_path: Path to system prompt file
        var_a_path: Path to Variable A context file
        var_b_path: Path to Variable B context file
        task_prompt_path: Path to task prompt file
        
    Returns:
        Tuple of (combined_prompt, var_a_name, var_b_name)
    """
    # Read all components
    system_prompt = read_file_content(system_prompt_path)
    var_a_content = read_file_content(var_a_path)
    var_b_content = read_file_content(var_b_path)
    task_prompt = read_file_content(task_prompt_path)
    
    # Get clean names for output
    var_a_name = extract_filename(var_a_path)
    var_b_name = extract_filename(var_b_path)
    
    # Combine all components
    combined = (
        f"{system_prompt}\n\n"
        f"VARIABLE A CONTEXT:\n{var_a_content}\n\n"
        f"VARIABLE B CONTEXT:\n{var_b_content}\n\n"
        f"TASK:\n{task_prompt}"
    )
    
    return combined, var_a_name, var_b_name
