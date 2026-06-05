from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def summarize_text(text):

    summary = summarizer(
        text,
        max_length=100,
        min_length=30,
        do_sample=False
    )

    return summary[0]['summary_text']

#This module provides a function to summarize text using the BART model from Hugging Face's transformers library. The summarize_text function takes a string of text as input and returns a summarized version of that text, with a maximum length of 100 words and a minimum length of 30 words.