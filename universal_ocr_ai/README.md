# Universal OCR AI

A Deep Learning based OCR + Translation + Summarization + QA System.

## Features

- OCR from images
- Translation
- Summarization
- Question Answering
- Streamlit UI

## Run Project

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## OCR Backends & Setup

### ✨ New: Automatic Fallback System

The OCR engine now intelligently falls back between OCR backends:

1. **Primary:** Tesseract (fast, lightweight, accurate for printed text)
2. **Fallback:** EasyOCR (neural, more accurate for complex/handwritten text)

**Setup:**

- **Option 1: No setup required** (recommended for quick start)
  - EasyOCR is now included in `requirements.txt` and will download the model on first use (~30-60 seconds).
  - If Tesseract is not installed, the app automatically uses EasyOCR.

- **Option 2: Use Tesseract only (faster, no model download)**
  - Download Tesseract from https://github.com/tesseract-ocr/tesseract/releases
  - Windows: Run the installer and add to PATH, or set:
    ```powershell
    setx TESSERACT_CMD "C:\Program Files\Tesseract-OCR\tesseract.exe"
    ```
  - Restart PowerShell after setting `TESSERACT_CMD`

- **Option 3: Force EasyOCR backend** (if Tesseract fails)
  - Set environment variable: `OCR_BACKEND=easyocr`

### Performance Notes

- **Streamlit startup is faster** because heavy Hugging Face pipelines (translation, summarization, QA) are now lazily loaded on first use.
- **EasyOCR on first run** will download the model (~60-100 MB), which takes a few minutes. Subsequent runs are fast.
- **GPU acceleration available** - set `OCR_EASYOCR_GPU=1` if you have CUDA installed.