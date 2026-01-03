import PyPDF2
import re

SKILLS = ["python", "java", "sql", "html", "css", "javascript", "machine learning", "flask"]

def parse_resume(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text().lower()
    return [s for s in SKILLS if re.search(rf"\b{s}\b", text)]
