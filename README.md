# Google Ads Copy Generator

A small Flask app that creates Google Ads style headlines and descriptions from your keywords.

## Features

- Keyword-driven ad copy generation.
- Character limit handling:
  - Headlines limited to 30 characters.
  - Descriptions limited to 90 characters.
- Configurable number of generated headlines/descriptions.
- Simple web UI.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5000>.
