# IMAGEGENAI

A simple Python Streamlit app that clones the style/composition of a reference image while keeping your AI model identity, powered by Replicate.

## Features

- **Tab 1: Cloner**
  - Upload a reference image.
  - Click **Create image of my AI model**.
  - App sends prompt + image inputs to Replicate and renders the generated output.
- **Tab 2: Setting**
  - Upload AI model face image.
  - Add your model **Master DNA** (identity prompt).
  - Add **Replicate API key**.
  - Choose a Replicate model slug.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## How to get a Replicate API key

1. Sign in or create an account at [https://replicate.com](https://replicate.com).
2. Open your account settings: [https://replicate.com/account/api-tokens](https://replicate.com/account/api-tokens).
3. Click **Create token**.
4. Copy the token and paste it into the app's **Replicate API key** field.

You can also export it in your terminal:

```bash
export REPLICATE_API_TOKEN="r8_..."
```

The app auto-fills the API key from this environment variable when available.

## Notes

- Different Replicate models accept different input names. Default is set to `black-forest-labs/flux-kontext-max`; if a model rejects the request, switch model slug.
- This app keeps settings in the Streamlit session state (browser session only).
