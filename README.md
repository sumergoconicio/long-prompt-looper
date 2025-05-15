# Prompt Chaining System

> **A modular system for generating LLM responses by chaining prompts with different combinations of context variables.**

---

## Table of Contents

1. [About](#about)  
2. [Features](#features)  
3. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Installation](#installation)  
   - [Configuration](#configuration)  
4. [Usage](#usage)  
5. [Project Structure](#project-structure)
6. [License](#license)  

---

## About

The Prompt Chaining System is designed to automate the process of generating multiple LLM responses by systematically combining different context variables. It's particularly useful for tasks that require testing how an LLM responds to various combinations of input contexts.

Key use cases:
- Testing model responses across different scenarios
- Generating training data with varied contexts
- Systematic exploration of model behavior with different input combinations

---

## Features

- **Modular Design** – Separate components for input handling, prompt construction, model querying, and output saving
- **Flexible Configuration** – Support for different LLM providers through adapters
- **Progress Tracking** – Real-time progress updates and logging
- **Error Handling** – Robust error handling and logging for reliable batch processing
- **Extensible** – Easy to add new model adapters or modify the processing pipeline

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sumergoconicio/long-prompt-looper.git
   cd long-prompt-looper
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

### Configuration

1. **Environment Variables** (in `.env`):
   - `OPENAI_API_KEY`: Your OpenAI API key (required for default LiteLLM adapter)
   - `LOG_LEVEL`: Logging level (default: INFO)

2. **File Structure**:
   ```
   project/
   ├── inputs/
   │   ├── var_a/       # Variable A context files
   │   ├── var_b/       # Variable B context files
   │   ├── system_prompt.txt
   │   └── task_prompt.txt
   └── outputs/         # Generated outputs
   ```

---

## Usage

1. Prepare your input files:
   - Place Variable A context files in `inputs/var_a/`
   - Place Variable B context files in `inputs/var_b/`
   - Create `system_prompt.txt` and `task_prompt.txt` in `inputs/`

2. Run the system:
   ```bash
   python main.py
   ```

3. Edit `user_inputs/user_inputs.json` to specify all required paths and prompt files. Example template:
   ```json
   {
     "var_a_dir": "inputs/var_a",
     "var_b_dir": "inputs/var_b",
     "output_dir": "outputs",
     "system_prompt": "inputs/system_prompt.txt",
     "task_prompt": "inputs/task_prompt.txt"
   }
   ```
   All runs are non-interactive and fully reproducible.

4. Run the system:
   ```bash
   python main.py
   ```

5. Monitor progress in the console and check output files in your specified output directory.

## Project Structure

```
prompt-chaining-system/
├── core/                   # Core functionality
│   ├── __init__.py
│   ├── get_inputs.py       # Input handling
│   ├── prompt_combiner.py  # Prompt construction
│   ├── query_model.py      # Model interaction
│   └── save_response.py    # Output handling
├── adapters/               # Model adapters
│   ├── __init__.py
│   └── select_model.py     # LiteLLM adapter
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.