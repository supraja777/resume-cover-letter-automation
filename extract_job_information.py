import json
from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

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


def extract_job_information(llm, filtered_jobs_path: str, JOB_INFORMATION_PATH: str):
    with open(filtered_jobs_path, "r", encoding="utf-8") as f:
            jobs = json.load(f)

    extract_application_information_chain = web_extraction_template | llm.with_structured_output(jobInformation)

    # print(job_urls)

    job_information = []

    for job in jobs:
        job_url = job.get("url", 0)
        company_name = job.get("company_name", 0)
        
        input_data = {"url": job_url}
        application_information = extract_application_information_chain.invoke(input_data)
        job_information.append([job_url, application_information.job_info])
        # print("Application information - ", application_information)

    # print(job_information)

    json_compatible = [[url, info] for url, info in job_information]

    with open(JOB_INFORMATION_PATH, "w", encoding="utf-8") as f:
            json.dump(json_compatible, f, indent=2)