import json
from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

from send_pdf_gmail import send_pdf_gmail

from pathlib import Path
import json

from convert_to_pdf import cover_letter_to_pdf

class CoverLetter(BaseModel):
    cover_letter: str = Field(..., description="Generated cover letter here")

create_cover_letter_template = PromptTemplate(
    input_variables = ["job_information", "resume"],
    template = """
    You are an expert career assistant specialized in writing professional and compelling cover letters.

    You will write the cover letter using attached resume. 
    
    Task:
    Using the job information provided, generate a **well-structured, tailored cover letter** that highlights the candidate's skills, experience, and enthusiasm for the role. The cover letter should:

    1. Be addressed to a general hiring manager (or use the company name if available).
    2. Clearly reference the **role** and **company**.
    3. Emphasize the candidate's relevant **technical and soft skills**.
    4. Highlight experience or qualifications that match the **responsibilities and requirements** mentioned in the job information.
    5. Be professional, concise, and engaging (roughly 250–400 words).
    6. Avoid repeating generic phrases; make it specific to the job and company.

    Job information:

    {job_information}

    Resume: 

    {resume}

    Output format:
    
    """
)

def create_cover_letter(url, job_information, llm, resume):
    input_data  = {"job_information": job_information, "resume": resume}
    create_cover_letter_chain = create_cover_letter_template | llm.with_structured_output(CoverLetter)

    return create_cover_letter_chain.invoke(input_data).cover_letter

def generate_cover_letter(llm, resume, service):
    with open("job_information.json", "r", encoding="utf-8") as f:
        all_jobs = json.load(f)
    
    cover_letters = []
    cnt = 1

    for job in all_jobs:
        url = job[0]
        job_information = job[1]

        # print("Job information == ", job_information)

        cover_letter = create_cover_letter(url, job_information, llm, resume)

        job_name = "XYZ"
        cnt+=1
        job_role = "Software developer.pdf"

        cover_letter_to_pdf(cover_letter,  job_name + str(cnt) + job_role)

        print("SENDING COVER LETTER === ", cnt)

        send_pdf_gmail(
            service=service,
            to_email="suprajasrikanth872@gmail.com",
            subject="Cover Letter – Application",
            body="Please find my cover letter attached.",
            pdf_path="Cover_Letter.pdf"
        )

        cover_letters.append([url, cover_letter])

    json_compatible = [[url, cover_letter] for url, cover_letter in cover_letters]
    # Save to a separate JSON file
    output_file = Path("cover_letters.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_compatible, f, indent=2)


