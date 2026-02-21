import io
import os
from typing import Any

import replicate
import requests
import streamlit as st
from PIL import Image

st.set_page_config(page_title="IMAGEGENAI Cloner", page_icon="🧬", layout="wide")

st.title("🧬 IMAGEGENAI")
st.caption("Create AI model images inspired by your reference image using Replicate.")

if "model_face" not in st.session_state:
    st.session_state.model_face = None
if "model_face_name" not in st.session_state:
    st.session_state.model_face_name = ""
if "master_dna" not in st.session_state:
    st.session_state.master_dna = ""
if "replicate_api_key" not in st.session_state:
    st.session_state.replicate_api_key = os.getenv("REPLICATE_API_TOKEN", "")
if "replicate_model" not in st.session_state:
    st.session_state.replicate_model = "black-forest-labs/flux-kontext-max"


def _normalize_output(output: Any) -> str | None:
    if output is None:
        return None
    if isinstance(output, str):
        return output
    if isinstance(output, list) and output:
        first = output[0]
        return str(first)
    return str(output)


def _download_image(image_url: str) -> Image.Image:
    response = requests.get(image_url, timeout=60)
    response.raise_for_status()
    return Image.open(io.BytesIO(response.content))


tab_cloner, tab_settings = st.tabs(["1. Cloner", "2. Setting"])

with tab_settings:
    st.subheader("AI Model Settings")

    model_face = st.file_uploader(
        "Upload AI model face", type=["png", "jpg", "jpeg"], key="model_face_upload"
    )
    if model_face:
        st.session_state.model_face = model_face.getvalue()
        st.session_state.model_face_name = model_face.name

    if st.session_state.model_face:
        st.image(st.session_state.model_face, caption="Current AI model face", width=260)

    st.session_state.master_dna = st.text_area(
        "Master DNA (describe your AI model identity)",
        value=st.session_state.master_dna,
        placeholder="Example: Futuristic fashion model, short silver hair, soft cinematic lighting...",
        height=140,
    )

    st.session_state.replicate_api_key = st.text_input(
        "Replicate API key",
        value=st.session_state.replicate_api_key,
        type="password",
        help="Get this from Replicate dashboard > API tokens.",
    )

    st.session_state.replicate_model = st.text_input(
        "Replicate model slug",
        value=st.session_state.replicate_model,
        help="Format: owner/model-name",
    )

with tab_cloner:
    st.subheader("Reference-based image generation")

    reference_image = st.file_uploader(
        "Upload reference image", type=["png", "jpg", "jpeg"], key="reference_image_upload"
    )

    col1, col2 = st.columns(2)
    with col1:
        if reference_image:
            st.image(reference_image, caption="Reference image", use_container_width=True)
    with col2:
        if st.session_state.model_face:
            st.image(st.session_state.model_face, caption="AI model face", use_container_width=True)

    generate_clicked = st.button("Create image of my AI model", type="primary")

    if generate_clicked:
        if not reference_image:
            st.error("Please upload a reference image in Cloner tab.")
        elif not st.session_state.model_face:
            st.error("Please upload AI model face in Setting tab.")
        elif not st.session_state.master_dna.strip():
            st.error("Please add Master DNA in Setting tab.")
        elif not st.session_state.replicate_api_key.strip():
            st.error("Please add your Replicate API key in Setting tab.")
        else:
            prompt = (
                "Create an image with the same composition, camera framing, outfit style, and mood "
                "as the reference image. The subject must look like this AI model face and follow this "
                f"master DNA description: {st.session_state.master_dna}. "
                "Keep photoreal quality and preserve facial identity strongly."
            )

            with st.spinner("Generating with Replicate..."):
                try:
                    client = replicate.Client(api_token=st.session_state.replicate_api_key)
                    output = client.run(
                        st.session_state.replicate_model,
                        input={
                            "prompt": prompt,
                            "input_image": reference_image,
                            "image": reference_image,
                        },
                    )
                    image_url = _normalize_output(output)
                    if not image_url:
                        st.error("Replicate returned no output image.")
                    else:
                        generated = _download_image(image_url)
                        st.success("Image generated successfully.")
                        st.image(generated, caption="Generated AI model image", use_container_width=True)
                        st.markdown(f"Output URL: {image_url}")
                except Exception as exc:
                    st.error(
                        "Generation failed. Verify your API key and model slug, then try again. "
                        f"Details: {exc}"
                    )
