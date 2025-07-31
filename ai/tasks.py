from celery import shared_task
from .summary import summarize_text
from documents.models import Document

@shared_task
def generate_summary(document_id):
    doc = Document.objects.get(id=document_id)
    with doc.file.open("r") as f:
        text = f.read()
    summary = summarize_text(text)
    doc.summary = summary
    doc.save()
    return summary
