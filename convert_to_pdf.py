from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path

# Creates a directory for coverletters and 
# Converts the given text and saves as pdf

def cover_letter_to_pdf(cover_letter_text, pdf_path):
   

    doc = SimpleDocTemplate(str(pdf_path))

    styles = getSampleStyleSheet()
    story = []

    for line in cover_letter_text.split("\n"):
        story.append(Paragraph(line.replace("&", "&amp;"), styles["Normal"]))

    doc.build(story)
