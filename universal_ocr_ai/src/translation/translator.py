from transformers import pipeline

translator = pipeline(
    task="translation_en_to_hi",
    model="Helsinki-NLP/opus-mt-en-hi"
)

def translate_text(text):

    result = translator(text)

    return result[0]['translation_text']