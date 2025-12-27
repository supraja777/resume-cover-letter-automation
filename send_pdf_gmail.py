import base64
from email.message import EmailMessage
from pathlib import Path

def send_pdf_gmail(
    service,
    to_email,
    subject,
    body,
    pdf_path
):
    message = EmailMessage()
    message["To"] = to_email
    message["From"] = "me"
    message["Subject"] = subject
    message.set_content(body)

    pdf_path = Path(pdf_path)
    with open(pdf_path, "rb") as f:
        message.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=pdf_path.name
        )

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": encoded_message}
    ).execute()
