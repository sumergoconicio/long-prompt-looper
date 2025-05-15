#!/usr/bin/env python3
"""
Prompt Chaining System

A modular system for generating LLM responses by chaining prompts with different
combinations of context variables.

Author: ChAI-Engine (chaiji)
Last Updated: 2025-05-15

Abstract Spec:
- Loads environment variables from .env using python-dotenv.
- Requires GEMINI_API_KEY for Gemini model usage.
- See /dev/project-brief.md for full configuration and environment details.
"""

import os
import sys
import logging
import time
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from dotenv import load_dotenv  # Non-standard dependency: python-dotenv

# Load environment variables from .env at startup
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('prompt_chain.log')
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path
sys.path.append(str(Path(__file__).parent.absolute()))

# Import core modules
from core import (
    get_user_inputs,
    combine_prompts,
    query_model,
    save_response
)
from adapters import set_default_adapter

def setup_model() -> None:
    """Set up the model adapter with default parameters."""
    try:
        # Set up the default model adapter (LiteLLM)
        # You can customize the model and parameters here
        set_default_adapter(
            model_name="gpt-4.1",
            temperature=0.7,
            max_tokens=32768,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        logger.info("Model adapter initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize model adapter: {str(e)}")
        raise

def process_combination(
    system_prompt_path: str,
    task_prompt_path: str,
    var_a_path: str,
    var_b_path: str,
    output_dir: str
) -> Optional[str]:
    """Process a single combination of Variable A and Variable B.
    
    Args:
        system_prompt_path: Path to system prompt file
        task_prompt_path: Path to task prompt file
        var_a_path: Path to Variable A context file
        var_b_path: Path to Variable B context file
        output_dir: Directory to save output files
        
    Returns:
        str: Path to the saved output file, or None if failed
    """
    try:
        # Combine all prompt components
        current_prompt, var_a_name, var_b_name = combine_prompts(
            system_prompt_path=system_prompt_path,
            var_a_path=var_a_path,
            var_b_path=var_b_path,
            task_prompt_path=task_prompt_path
        )
        
        logger.debug(f"Generated prompt for {var_a_name} x {var_b_name}")
        
        # Query the model
        response = query_model(current_prompt)
        
        # Save the response
        output_path = save_response(
            content=response,
            output_dir=output_dir,
            var_a_name=var_a_name,
            var_b_name=var_b_name
        )
        
        logger.info(f"Completed processing: {var_a_name} x {var_b_name}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error processing {var_a_path} x {var_b_path}: {str(e)}")
        return None

def main():
    """Main entry point for the prompt chaining system.
    
    Fails gracefully if VariableA or VariableB folders are empty, and continues with just system prompt and task prompt.
    """
    try:
        print("\n=== Prompt Chaining System ===\n")
        print("[INFO] This program now loads all input paths from user_inputs.json at project root.\nIf user_inputs.json does not exist, a template will be created for you to fill in.\n")
        
        # Set up the model
        setup_model()
        
        # Get user inputs from config
        inputs = get_user_inputs()
        
        # Get lists of context files
        from core.get_inputs import get_context_files
        var_a_files, var_b_files = get_context_files(
            inputs['var_a_dir'], 
            inputs['var_b_dir']
        )

        completed = 0
        start_time = time.time()

        # Robust fallback logic
        if not var_a_files and not var_b_files:
            logger.warning("Both VariableA and VariableB folders are empty. Proceeding with only system prompt and task prompt.")
            print("[WARNING] Both VariableA and VariableB folders are empty. Proceeding with only system prompt and task prompt.")
            output_path = process_combination(
                system_prompt_path=inputs['system_prompt'],
                task_prompt_path=inputs['task_prompt'],
                var_a_path=None,
                var_b_path=None,
                output_dir=inputs['output_dir']
            )
            if output_path:
                completed = 1
                print(f"Processed {completed}/1: {os.path.basename(output_path)}")
            elapsed = time.time() - start_time
            print(f"\n=== Processing Complete (Fallback Mode) ===")
            print(f"Total combinations processed: {completed}/1")
            print(f"Time taken: {elapsed:.2f} seconds")
            print(f"Output directory: {inputs['output_dir']}")
            return
        elif not var_a_files:
            logger.warning("VariableA folder is empty. Proceeding with only VariableB files.")
            print("[WARNING] VariableA folder is empty. Proceeding with only VariableB files.")
            total_combinations = len(var_b_files)
            for var_b_path in var_b_files:
                output_path = process_combination(
                    system_prompt_path=inputs['system_prompt'],
                    task_prompt_path=inputs['task_prompt'],
                    var_a_path=None,
                    var_b_path=var_b_path,
                    output_dir=inputs['output_dir']
                )
                if output_path:
                    completed += 1
                    print(f"Processed {completed}/{total_combinations}: {os.path.basename(output_path)}")
            elapsed = time.time() - start_time
            print(f"\n=== Processing Complete (Fallback Mode) ===")
            print(f"Total combinations processed: {completed}/{total_combinations}")
            print(f"Time taken: {elapsed:.2f} seconds")
            print(f"Output directory: {inputs['output_dir']}")
            return
        elif not var_b_files:
            logger.warning("VariableB folder is empty. Proceeding with only VariableA files.")
            print("[WARNING] VariableB folder is empty. Proceeding with only VariableA files.")
            total_combinations = len(var_a_files)
            for var_a_path in var_a_files:
                output_path = process_combination(
                    system_prompt_path=inputs['system_prompt'],
                    task_prompt_path=inputs['task_prompt'],
                    var_a_path=var_a_path,
                    var_b_path=None,
                    output_dir=inputs['output_dir']
                )
                if output_path:
                    completed += 1
                    print(f"Processed {completed}/{total_combinations}: {os.path.basename(output_path)}")
            elapsed = time.time() - start_time
            print(f"\n=== Processing Complete (Fallback Mode) ===")
            print(f"Total combinations processed: {completed}/{total_combinations}")
            print(f"Time taken: {elapsed:.2f} seconds")
            print(f"Output directory: {inputs['output_dir']}")
            return
        else:
            total_combinations = len(var_a_files) * len(var_b_files)
            print(f"\nWill process {total_combinations} combinations...")
            for var_a_path in var_a_files:
                for var_b_path in var_b_files:
                    output_path = process_combination(
                        system_prompt_path=inputs['system_prompt'],
                        task_prompt_path=inputs['task_prompt'],
                        var_a_path=var_a_path,
                        var_b_path=var_b_path,
                        output_dir=inputs['output_dir']
                    )
                    if output_path:
                        completed += 1
                        print(f"Processed {completed}/{total_combinations}: {os.path.basename(output_path)}")
            elapsed = time.time() - start_time
            print(f"\n=== Processing Complete ===")
            print(f"Total combinations processed: {completed}/{total_combinations}")
            print(f"Time taken: {elapsed:.2f} seconds")
            print(f"Average time per combination: {elapsed/max(1, completed):.2f} seconds")
            print(f"Output directory: {inputs['output_dir']}")
        
    except ValueError as e:
        logger.error(str(e))
        print(f"[ERROR] {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        print("[ERROR] An unexpected error occurred. See log for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
