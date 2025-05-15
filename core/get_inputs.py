"""
Module for handling user input collection and validation.

Now supports config-driven input via user_inputs/user_inputs.json.
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
import sys

CONFIG_PATH = os.path.join("user_inputs", "user_inputs.json")

def validate_directory(path: str, name: str) -> str:
    """Validate if the provided path is a valid directory.
    
    Args:
        path: Path to validate
        name: Name of the directory for error messages
        
    Returns:
        str: Validated absolute path
        
    Raises:
        ValueError: If directory doesn't exist or is not accessible
    """
    try:
        abs_path = os.path.abspath(path)
        if not os.path.isdir(abs_path):
            raise ValueError(f"{name} directory does not exist: {abs_path}")
        return abs_path
    except Exception as e:
        raise ValueError(f"Error accessing {name} directory: {str(e)}")

def validate_file(path: str, name: str) -> str:
    """Validate if the provided path is a valid file.
    
    Args:
        path: Path to validate
        name: Name of the file for error messages
        
    Returns:
        str: Validated absolute path
        
    Raises:
        ValueError: If file doesn't exist or is not accessible
    """
    try:
        abs_path = os.path.abspath(path)
        if not os.path.isfile(abs_path):
            raise ValueError(f"{name} file does not exist: {abs_path}")
        return abs_path
    except Exception as e:
        raise ValueError(f"Error accessing {name} file: {str(e)}")

def load_user_inputs_from_json(json_path: str = CONFIG_PATH) -> Dict[str, str]:
    """
    Load and validate user inputs from a JSON config file at user_inputs/user_inputs.json.
    If the config does not exist, generate a template and exit.
    Args:
        json_path: Path to the user_inputs.json file (default: user_inputs/user_inputs.json)
    Returns:
        Dict containing all validated input paths
    Raises:
        SystemExit: If validation fails or config is missing/incomplete
    """
    required_keys = [
        "var_a_dir",
        "var_b_dir",
        "output_dir",
        "system_prompt",
        "task_prompt"
    ]
    if not os.path.exists(json_path):
        print(f"\nuser_inputs.json config not found at {json_path}.")
        generate_user_inputs_template(json_path)
        print("Please fill in the required paths in the generated template and re-run the program.")
        sys.exit(1)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        # Validate required keys
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required key: {key}")
        # Validate paths
        validated = {}
        validated['var_a_dir'] = validate_directory(config['var_a_dir'], "Variable A")
        validated['var_b_dir'] = validate_directory(config['var_b_dir'], "Variable B")
        validated['output_dir'] = validate_directory(config['output_dir'], "Output")
        validated['system_prompt'] = validate_file(config['system_prompt'], "System prompt")
        validated['task_prompt'] = validate_file(config['task_prompt'], "Task prompt")
        return validated
    except ValueError as e:
        print(f"\nError: {str(e)}")
        print(f"Please check the paths in {json_path} and try again.")
        sys.exit(1)


def generate_user_inputs_template(json_path: str = CONFIG_PATH) -> None:
    """
    Generate a template user_inputs.json config file at user_inputs/user_inputs.json.
    Args:
        json_path: Path to write the template (default: user_inputs/user_inputs.json)
    """
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    template = {
        "var_a_dir": "<absolute/path/to/variable_a_context_directory>",
        "var_b_dir": "<absolute/path/to/variable_b_context_directory>",
        "output_dir": "<absolute/path/to/output_directory>",
        "system_prompt": "<absolute/path/to/system_prompt.txt>",
        "task_prompt": "<absolute/path/to/task_prompt.txt>"
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2)
    print(f"Template user_inputs.json written to {json_path}")


def get_user_inputs() -> Dict[str, str]:
    """
    Load and validate user inputs from user_inputs/user_inputs.json.
    Returns:
        Dict containing all validated input paths
    Raises:
        SystemExit: If validation fails or config is missing/incomplete
    """
    return load_user_inputs_from_json(CONFIG_PATH)


def get_context_files(var_a_dir: str, var_b_dir: str) -> Tuple[List[str], List[str]]:
    """Get lists of context files from the input directories.
    
    Args:
        var_a_dir: Path to Variable A directory
        var_b_dir: Path to Variable B directory
        
    Returns:
        Tuple of (var_a_files, var_b_files)
        
    Raises:
        ValueError: If no valid files found in either directory
    """
    def get_txt_md_files(directory: str) -> List[str]:
        return sorted([
            os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) 
            and f.lower().endswith(('.txt', '.md'))
        ])
    
    var_a_files = get_txt_md_files(var_a_dir)
    var_b_files = get_txt_md_files(var_b_dir)
    
    if not var_a_files:
        raise ValueError(f"No .txt or .md files found in Variable A directory: {var_a_dir}")
    if not var_b_files:
        raise ValueError(f"No .txt or .md files found in Variable B directory: {var_b_dir}")
    
    print(f"\nFound {len(var_a_files)} Variable A files and {len(var_b_files)} Variable B files")
    return var_a_files, var_b_files
