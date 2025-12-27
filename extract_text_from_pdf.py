from PyPDF2 import PdfReader

def extract_text_from_pdf(llm, pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)