import sys
import os
from pathlib import Path

# Ensure the project root is on sys.path so `from src...` imports work when
# Streamlit runs the script from the `app/` directory.
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from PIL import Image

from src.ocr.ocr_engine import extract_text
from src.utils.logger import logger
# from src.translation.translator import translate_text
# from src.summarization.summarizer import summarize_text
# from src.question_answering.qa_engine import ask_question

st.set_page_config(
    page_title="Universal OCR AI",
    layout="wide"
)

st.title("Universal OCR AI System")

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image")

    save_path = f"data/raw/{uploaded_file.name}"

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Image Uploaded Successfully")

    if st.button("Run OCR"):

        with st.spinner("Extracting Text..."):
            try:
                result = extract_text(save_path)
                full_text = ""
                for item in result:
                    full_text += item.get("text", "") + " "

                st.subheader("Extracted Text")
                st.write(full_text)
                st.session_state['ocr_text'] = full_text
            except Exception as e:
                logger.exception("Streamlit OCR failed")
                error_msg = str(e)
                st.error(
                    f"❌ OCR Processing Failed\n\n{error_msg}\n\n"
                    "**Solutions:**\n"
                    "- If using Tesseract: Install from https://github.com/tesseract-ocr/tesseract/releases\n"
                    "- If using EasyOCR: It will download the model on first use (may take a few minutes)\n"
                    "- Check the terminal logs for more details"
                )

if 'ocr_text' in st.session_state:

    st.divider()

    st.subheader("Translation")

    if st.button("Translate to Hindi"):
        try:
            from src.translation.translator import translate_text
            translated = translate_text(st.session_state['ocr_text'])
            st.write(translated)
        except Exception as e:
            logger.exception("Translation failed")
            st.error(f"Translation failed: {e}")

    st.divider()

    st.subheader("Summarization")

    if st.button("Generate Summary"):
        try:
            from src.summarization.summarizer import summarize_text
            summary = summarize_text(st.session_state['ocr_text'])
            st.write(summary)
        except Exception as e:
            logger.exception("Summarization failed")
            st.error(f"Summarization failed: {e}")

    st.divider()

    st.subheader("Ask Questions")

    question = st.text_input(
        "Ask Question from Document"
    )

    if st.button("Get Answer"):
        try:
            from src.question_answering.qa_engine import ask_question
            answer = ask_question(st.session_state['ocr_text'], question)
            st.write(answer)
        except Exception as e:
            logger.exception("QA failed")
            st.error(f"Question-answering failed: {e}")