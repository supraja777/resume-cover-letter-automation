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