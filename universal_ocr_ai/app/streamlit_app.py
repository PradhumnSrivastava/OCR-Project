import streamlit as st
import os
from PIL import Image

from src.ocr.paddleocr_engine import extract_text
from src.translation.translator import translate_text
from src.summarization.summarizer import summarize_text
from src.question_answering.qa_engine import ask_question

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

            result = extract_text(save_path)

            full_text = ""

            for item in result:

                full_text += item['text'] + " "

            st.subheader("Extracted Text")

            st.write(full_text)

            st.session_state['ocr_text'] = full_text

if 'ocr_text' in st.session_state:

    st.divider()

    st.subheader("Translation")

    if st.button("Translate to Hindi"):

        translated = translate_text(
            st.session_state['ocr_text']
        )

        st.write(translated)

    st.divider()

    st.subheader("Summarization")

    if st.button("Generate Summary"):

        summary = summarize_text(
            st.session_state['ocr_text']
        )

        st.write(summary)

    st.divider()

    st.subheader("Ask Questions")

    question = st.text_input(
        "Ask Question from Document"
    )

    if st.button("Get Answer"):

        answer = ask_question(
            st.session_state['ocr_text'],
            question
        )

        st.write(answer)