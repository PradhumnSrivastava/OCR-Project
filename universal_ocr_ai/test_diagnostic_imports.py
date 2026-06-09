#!/usr/bin/env python
"""Diagnostic test to identify import blocking issues."""
import sys
from pathlib import Path

PROJECT_ROOT = str(Path(__file__).resolve().parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("Diagnostic Import Test")
print("=" * 60)

tests = [
    ("os", lambda: __import__("os")),
    ("sys", lambda: __import__("sys")),
    ("pathlib", lambda: __import__("pathlib")),
    ("PIL", lambda: __import__("PIL")),
    ("cv2", lambda: __import__("cv2")),
    ("numpy", lambda: __import__("numpy")),
    ("logging", lambda: __import__("logging")),
]

for name, test_fn in tests:
    try:
        print(f"Importing {name}...", end=" ", flush=True)
        test_fn()
        print("✓")
    except Exception as e:
        print(f"✗ FAILED: {e}")

print("=" * 60)
print("All basic imports OK. Trying src.utils.logger...")
try:
    from src.utils.logger import logger
    print("✓ src.utils.logger imported")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\nTrying src.ocr.ocr_engine import...")
try:
    from src.ocr.ocr_engine import OCREngine
    print("✓ OCREngine imported (this triggers module-level _engine creation)")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\nDone!")
