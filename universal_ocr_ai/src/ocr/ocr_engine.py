import os
from PIL import Image
import cv2
import numpy as np
import logging

try:
    import pytesseract
except Exception:
    pytesseract = None

from src.utils.logger import logger


class OCREngine:
    """Simple modular OCR engine.

    - Default backend: `tesseract` (requires Tesseract installed on the system).
    - Optional backend: `easyocr` (if installed).

    The engine uses lazy initialization and lightweight preprocessing for
    improved stability and startup speed on Windows.
    """

    def __init__(self, backend: str = None):
        self.backend = backend or os.environ.get("OCR_BACKEND", "tesseract")
        self._ready = False
        self.model = None

    def _init_tesseract(self):
        if pytesseract is None:
            raise RuntimeError("pytesseract is not installed. Install it or set OCR_BACKEND=easyocr")
        # allow user to override the tesseract executable path via env var
        cmd = os.environ.get("TESSERACT_CMD")
        if cmd:
            pytesseract.pytesseract.tesseract_cmd = cmd
            logger.info(f"Using Tesseract binary from TESSERACT_CMD={cmd}")
        # Note: actual Tesseract availability will be tested during first extraction
        # and will fallback to EasyOCR if not found
        self._ready = True

    def _init_easyocr(self):
        try:
            import easyocr
        except Exception as e:
            raise RuntimeError("easyocr not available; install easyocr or use tesseract") from e
        # Use CPU by default for Windows stability; user can set OCR_EASYOCR_GPU=1 to enable GPU
        use_gpu = os.environ.get("OCR_EASYOCR_GPU", "0") == "1"
        self.model = easyocr.Reader(["en"], gpu=use_gpu)
        self._ready = True

    def _ensure_ready(self):
        if self._ready:
            return
        logger.info(f"Initializing OCR backend: {self.backend}")
        
        try:
            if self.backend == "tesseract":
                self._init_tesseract()
            elif self.backend == "easyocr":
                self._init_easyocr()
            else:
                raise ValueError(f"Unknown OCR backend: {self.backend}")
        except Exception as e:
            # If primary backend fails and is tesseract, try fallback to easyocr
            if self.backend == "tesseract":
                logger.warning(
                    f"Tesseract initialization failed ({e}). "
                    "Attempting to fall back to EasyOCR..."
                )
                try:
                    self.backend = "easyocr"
                    self._init_easyocr()
                    logger.info("Successfully switched to EasyOCR backend")
                except Exception as easyocr_err:
                    logger.error(f"EasyOCR fallback also failed: {easyocr_err}")
                    raise RuntimeError(
                        f"Both OCR backends failed:\n"
                        f"  Tesseract: {e}\n"
                        f"  EasyOCR: {easyocr_err}\n"
                        f"Please install Tesseract or EasyOCR. "
                        f"See README.md for instructions."
                    ) from easyocr_err
            else:
                raise

    def preprocess(self, image_path: str):
        # Read image with OpenCV for consistent preprocessing
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image not found: {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Downscale very large images to reduce processing time
        h, w = gray.shape[:2]
        max_dim = 1600
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

        # Denoise and binarize - lightweight and usually helps Tesseract
        gray = cv2.fastNlMeansDenoising(gray, None, h=10)
        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return th

    def extract_text(self, image_path: str):
        try:
            self._ensure_ready()

            if self.backend == "tesseract":
                try:
                    img = self.preprocess(image_path)
                    # Use Tesseract's TSV output to get per-word confidences
                    if pytesseract is None:
                        raise RuntimeError("pytesseract not present at runtime")
                    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                    results = []
                    n = len(data.get("text", []))
                    for i in range(n):
                        text = (data["text"][i] or "").strip()
                        if not text:
                            continue
                        # Tesseract may return '-1' for unknown/confidence
                        conf_raw = data["conf"][i]
                        try:
                            conf = float(conf_raw)
                        except Exception:
                            conf = 0.0
                        results.append({"text": text, "confidence": conf})
                    return results
                except Exception as tesseract_err:
                    # If Tesseract fails (e.g., not installed), try fallback to EasyOCR
                    if "tesseract" in str(tesseract_err).lower() or "not found" in str(tesseract_err).lower():
                        logger.warning(
                            f"Tesseract extraction failed ({tesseract_err}). "
                            "Attempting to switch to EasyOCR..."
                        )
                        try:
                            self.backend = "easyocr"
                            self._ready = False  # Force re-initialization
                            return self.extract_text(image_path)  # Retry with EasyOCR
                        except Exception as easyocr_err:
                            logger.error(f"EasyOCR fallback also failed: {easyocr_err}")
                            raise
                    else:
                        raise

            elif self.backend == "easyocr":
                # easyocr expects RGB PIL or numpy
                img = Image.open(image_path).convert("RGB")
                arr = np.array(img)
                raw = self.model.readtext(arr)
                results = []
                for bbox, text, conf in raw:
                    results.append({"text": text, "confidence": float(conf)})
                return results

        except Exception as e:
            logger.exception("OCR extraction failed")
            return [{"text": f"OCR Error: {str(e)}", "confidence": 0}]


# Module-level engine for simple usage in the codebase (lazy init)
_backend_choice = os.environ.get("OCR_BACKEND", "tesseract")
_engine = OCREngine(backend=_backend_choice)


def extract_text(image_path: str):
    """Convenience function kept for backward compatibility.

    Usage: `from src.ocr.ocr_engine import extract_text`
    """
    return _engine.extract_text(image_path)
