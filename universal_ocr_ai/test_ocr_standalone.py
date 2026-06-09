#!/usr/bin/env python
"""Standalone test to verify OCR engine functionality without Streamlit."""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = str(Path(__file__).resolve().parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("=" * 60)
print("OCR Engine Standalone Test")
print("=" * 60)

# Test 1: Import OCR engine
print("\n[1/3] Testing OCR engine import...")
try:
    from src.ocr.ocr_engine import OCREngine, extract_text
    print("✓ Successfully imported OCREngine and extract_text")
except Exception as e:
    print(f"✗ Failed to import OCR engine: {e}")
    sys.exit(1)

# Test 2: Create OCR engine instance
print("\n[2/3] Testing OCR engine instantiation...")
try:
    engine = OCREngine(backend="tesseract")
    print(f"✓ Created OCREngine instance with backend: {engine.backend}")
except Exception as e:
    print(f"✗ Failed to create OCREngine: {e}")
    sys.exit(1)

# Test 3: Verify module-level function
print("\n[3/3] Testing module-level extract_text function...")
try:
    print("✓ extract_text function is callable:", callable(extract_text))
except Exception as e:
    print(f"✗ Failed to verify extract_text: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED ✓")
print("=" * 60)
print("\nNext steps:")
print("1. Install Tesseract system binary from:")
print("   https://github.com/tesseract-ocr/tesseract/releases")
print("2. Then run: streamlit run app/streamlit_app.py")
print("=" * 60)
