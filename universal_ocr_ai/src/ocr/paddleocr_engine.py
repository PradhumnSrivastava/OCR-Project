import os
from src.utils.logger import logger

# Make importing this file safe even when PaddleOCR is not available on the
# system (Paddle is known to be unstable on Windows / Python 3.11). This
# module remains as a compatibility wrapper but the project uses
# `src.ocr.ocr_engine` by default.

try:
    os.environ["FLAGS_use_mkldnn"] = "0"
    from paddleocr import PaddleOCR
    _paddle_available = True
except Exception as _err:
    PaddleOCR = None
    _paddle_available = False
    logger = logger
    logger = logger


def extract_text(image_path):
    """Compatibility wrapper for PaddleOCR.

    If PaddleOCR is not available this returns an error message telling the
    caller to use the more stable `src.ocr.ocr_engine` implementation.
    """
    if not _paddle_available:
        return [{
            "text": "PaddleOCR not available on this system. Install paddleocr/paddlepaddle or use the default Tesseract-based engine (set OCR_BACKEND) and ensure Tesseract is installed.",
            "confidence": 0
        }]

    try:
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        result = ocr.ocr(image_path)
        extracted_text = []
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                confidence = line[1][1]
                extracted_text.append({"text": text, "confidence": confidence})
        return extracted_text
    except Exception as e:
        logger.exception("PaddleOCR extraction failed")
        return [{"text": f"OCR Error: {str(e)}", "confidence": 0}]