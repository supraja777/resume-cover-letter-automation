import json
from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

from generate_cover_letter import create_cover_letter
from convert_to_pdf import cover_letter_to_pdf
from send_pdf_gmail import send_pdf_gmail
from pathlib import Path

class jobInformation(BaseModel):
    job_info: str = Field(..., description="Extracted job information text here")

web_extraction_template = PromptTemplate(
    input_variables = ["url"],
    template = """
    You are an expert at extracting job-related information from web content. 

    Your task is to read the provided web content and extract **all relevant details** about the job that would help someone understand the role and write a tailored application. This includes:

    - Detailed description of the role and responsibilities
    - Required technical and soft skills
    - Information about the company (overview, mission, culture, industry)
    - Any additional useful details (location, remote status, job type, application instructions, etc.)

    Combine all this information into a single, coherent paragraph and return it as **one field** called "job_info". Be precise, detailed, and only include information explicitly present in the content. Do NOT hallucinate or add anything that is not stated.

    url: {url}

    Output format:
        job_info :

    """
)

def convert_to_pdf_send_email(cover_letter, cover_letter_path, service):

    print(cover_letter_path)
    cover_letter_to_pdf(cover_letter, cover_letter_path)

    send_pdf_gmail(
        service=service,
        to_email="suprajasrikanth872@gmail.com",
        subject="Cover Letter – Application",
        body="Please find my cover letter attached.",
        pdf_path = cover_letter_path
    )

    # cover_letters.append([url, cover_letter])

def get_file_path(company_name:str, title:str):
    BASE_DIR = Path(__file__).resolve().parent
    COVER_LETTER_DIR = BASE_DIR / "cover_letter" / "outputs"
    COVER_LETTER_DIR.mkdir(parents=True, exist_ok=True)
    file_name = company_name + title + ".pdf"

    pdf_path = COVER_LETTER_DIR / file_name
    return pdf_path

def send_cv(llm, JOB_LISTING: str, resume, service):
    with open(JOB_LISTING, "r", encoding="utf-8") as f:
            jobs = json.load(f)

    extract_application_information_chain = web_extraction_template | llm.with_structured_output(jobInformation)

    jobs_posted_today = jobs[0:5]

    for job in jobs_posted_today:
        job_url = job.get("url", 0)
        company_name = job.get("company_name", 0)
        title = job.get("title", 0)

        input_data = {"url": job_url}
        application_information = extract_application_information_chain.invoke(input_data)

        cover_letter = create_cover_letter(job_url, application_information, llm, resume)

        file_path = get_file_path(company_name, title)

        if cover_letter:
             convert_to_pdf_send_email(cover_letter, file_path, service)
        else:
             print("Cover letter is NULL for ", job_url)
