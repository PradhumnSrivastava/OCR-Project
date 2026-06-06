import os

os.environ["FLAGS_use_mkldnn"] = "0"

from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en'
)

def extract_text(image_path):

    try:

        result = ocr.ocr(image_path)

        extracted_text = []

        if result and result[0]:

            for line in result[0]:

                text = line[1][0]
                confidence = line[1][1]

                extracted_text.append({
                    "text": text,
                    "confidence": confidence
                })

        return extracted_text

    except Exception as e:

        return [{
            "text": f"OCR Error: {str(e)}",
            "confidence": 0
        }]