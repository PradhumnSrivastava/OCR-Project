from transformers import pipeline

_translator = None

def _get_translator():
    global _translator
    if _translator is None:
        _translator = pipeline("translation_en_to_hi", model="Helsinki-NLP/opus-mt-en-hi")
    return _translator


def translate_text(text):
    translator = _get_translator()
    result = translator(text)
    return result[0]["translation_text"]