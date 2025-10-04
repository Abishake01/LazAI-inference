# Build_chill_w2 — LazAI/Alith Data Upload and Inference

This folder contains a minimal, end-to-end demo to:
- Encrypt a sample dataset, upload it to IPFS via Pinata, and register it with LazAI (mint DAT).
- Run inference against the registered DAT using an OpenAI-compatible endpoint.
- Optionally run a local server compatible with OpenAI client SDKs.

## Prerequisites
- Python 3.8+
- A LazAI wallet private key
- Pinata IPFS JWT token
- (Recommended) A Python virtual environment

## Folder Contents
- `Dat.py` — Encrypts sample privacy data, uploads to IPFS, registers file with LazAI, and prints the File ID.
- `inference.py` — Uses a File ID to call an inference node with settlement headers.
- `server.py` — Starts an OpenAI-compatible inference server via `alith`.
- `requirements.txt` — Python dependencies for this sub-project.
- `.env` — Local environment variables (not tracked; create your own values).

## Setup

1) Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate
```

2) Install dependencies
```bash
pip install -r requirements.txt
```

3) Configure environment variables
Create a `.env` file in this folder with the following keys:
```bash
PRIVATE_KEY=your_lazai_private_key_here
IPFS_JWT=your_pinata_jwt_here
```

## 1) Mint DAT (Upload + Register)
Run `Dat.py` to encrypt and upload the sample data, then register it with LazAI:
```bash
python Dat.py
```
Expected output includes a line like:
```
File ID: <number>
```
Copy and save this File ID for inference.

## 2) Run Inference
Update `file_id` in `inference.py` if needed, then run:
```bash
python inference.py
```
What it does:
- Ensures your LazAI user is registered and funded (see `DEPOSIT_AMOUNT`).
- Finds the inference node URL for the configured iDAO address.
- Sends a prompt to the model with settlement headers bound to your DAT `file_id`.

You should see output similar to the model response. In this sample, the prompt is:
```
Tell a pome about LazAI and Dat protocol
```

## 3) Optional: Run Local Inference Server
Start an OpenAI-compatible server:
```bash
python server.py
```
Adjust the model/engine in `server.py` as needed.

## Troubleshooting
- Ensure `.env` contains valid `PRIVATE_KEY` and `IPFS_JWT`.
- If user/account steps fail in `inference.py`, confirm you have sufficient test funds and correct iDAO address.
- If `File ID` is 0 or missing, re-run `Dat.py` and make sure upload succeeded.

## Notes
- Example iDAO address and models are provided in code. Replace with your own as required.
- Logs under any `llm_logs/` path may be gitignored. If you need to submit inference artifacts, copy queries/responses into a tracked markdown file (e.g., `inference_logs.md`).
