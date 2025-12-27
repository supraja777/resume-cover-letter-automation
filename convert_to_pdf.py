from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def cover_letter_to_pdf(cover_letter_text, output_path):
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    story = []

    for line in cover_letter_text.split("\n"):
        story.append(Paragraph(line.replace("&", "&amp;"), styles["Normal"]))

    doc.build(story)

    