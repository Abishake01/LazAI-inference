# Build_chill_w4 — Python Digital Twin

A Python CLI version of the Digital Twin found in `Build_chill_w4/` that uses the same `character.json` persona and `alith.Agent` to power conversations.

## Prerequisites
- Python 3.8+
- A Groq API key (recommended) or any OpenAI-compatible API key

## Setup

1) Create and activate a virtual environment
```powershell
python -m venv venv
venv\Scripts\activate
```

2) Install dependencies
```powershell
pip install -r requirements.txt
```

3) Set your API key
- Recommended (Groq):
  - Windows (PowerShell):
    ```powershell
    setx GROQ_API_KEY "your-groq-api-key"
    # in current session:
    $env:GROQ_API_KEY = "your-groq-api-key"
    ```
  - macOS/Linux:
    ```bash
    export GROQ_API_KEY="your-groq-api-key"
    ```

- Optional fallback (generic OpenAI-compatible):
  ```powershell
  setx OPENAI_API_KEY "your-openai-api-key"
  $env:OPENAI_API_KEY = "your-openai-api-key"
  ```

## Run
```powershell
python digital_twin.py
```
You will see a welcome banner. Type your messages and hit Enter. Type `exit` to quit.

## Files
- `digital_twin.py` — CLI app that loads `character.json`, builds a preamble, and chats via `alith.Agent`.
- `character.json` — The persona definition copied from the TS project.
- `requirements.txt` — Minimal dependencies.

## Notes
- The app uses Groq's OpenAI-compatible endpoint at `https://api.groq.com/openai/v1`.
- We automatically map `GROQ_API_KEY` -> `OPENAI_API_KEY` at runtime.
- Default model is `llama-3.3-70b-versatile`. You can adjust it in `digital_twin.py`.
- If you see an API key error, confirm `GROQ_API_KEY` (or `OPENAI_API_KEY`) is set and restart your terminal.
