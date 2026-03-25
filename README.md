# AI_Customer_Intelligence

This repository contains a small Python project for customer intelligence analysis. This README is written to help an assistant (or future contributor) understand the project structure, run it locally, and provide clear instructions when requesting code changes.

## Quick Overview
- **Purpose:** Analyze customer data and expose pages for registration, data engine, personas, and a marketplace view.
- **Primary entry:** [main.py](main.py)

## Project structure

- [main.py](main.py) — project entry script
- [requirements.txt](requirements.txt) — Python dependencies
- [data/customer_data.csv](data/customer_data.csv) — sample data
- [models/](models/) — trained models or model-related code
- pages/ — streamlit or page-like modules
  - [pages/1_Registration.py](pages/1_Registration.py)
  - [pages/2_Data_Engine.py](pages/2_Data_Engine.py)
  - [pages/3_Personas.py](pages/3_Personas.py)
  - [pages/4_Marketplace.py](pages/4_Marketplace.py)

## Setup (local)

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app (example):

```bash
python main.py
```

Adjust commands if you use Conda or a different OS shell.

## What to look at first when changing code

- Start with the page that corresponds to the feature (see `pages/` links above).
- Check `data/customer_data.csv` for sample records and expected column names.
- If behavior depends on models, inspect `models/` for loading or preprocessing.
- Use `requirements.txt` to ensure environment parity.

## Coding conventions & environment
- Python version: 3.8+ recommended.
- Formatting: prefer `black` and `flake8` for linting (not required, but helpful).
- Keep functions small and add docstrings for public functions/classes.

## How to request a change (please include these)
When you ask me to modify code, please include:

- **Target file(s):** link to file(s) (for example, [pages/1_Registration.py](pages/1_Registration.py)).
- **Desired behavior:** a short description and example input/output if applicable.
- **Runtime evidence:** any error messages, stack traces, or failing test output.
- **Priority & constraints:** performance, backward-compatibility, deadlines.

Example request: "Fix validation in [pages/1_Registration.py](pages/1_Registration.py) so empty emails raise ValidationError; sample input: blank email; current error: see traceback." 

## Testing & verifying changes
- If you add or change logic, include a small script or unit test demonstrating the expected behavior.
- I can run simple verification commands locally if you want me to run the project after edits.

## Next steps I can take for you
- Create or update this README with more project-specific details.
- Add a CONTRIBUTING.md or a basic test harness.
- Implement requested code changes, run the app, and provide a short report.

If you'd like, tell me which file to inspect or what change you want next.
