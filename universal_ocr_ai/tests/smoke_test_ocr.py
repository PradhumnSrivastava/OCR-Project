from PIL import Image, ImageDraw, ImageFont
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so `src` imports resolve when running
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.ocr.ocr_engine import extract_text


def make_test_image(path: str):
    img = Image.new("RGB", (600, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    text = "Hello 123"
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except Exception:
        font = ImageFont.load_default()
    d.text((10, 60), text, fill=(0, 0, 0), font=font)
    img.save(path)


def main():
    os.makedirs("data/raw", exist_ok=True)
    path = "data/raw/test_ocr.png"
    make_test_image(path)
    print("Saved test image to", path)
    results = extract_text(path)
    print("OCR results:")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
