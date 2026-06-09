from transformers import pipeline

_qa_pipeline = None

def _get_qa_pipeline():
    global _qa_pipeline
    if _qa_pipeline is None:
        _qa_pipeline = pipeline("question-answering")
    return _qa_pipeline


def ask_question(context, question):
    qa = _get_qa_pipeline()
    result = qa(question=question, context=context)
    return result["answer"]