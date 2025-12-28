from extract_job_information import extract_job_information
from load_job_listing import fetch_and_save_json, filter_jobs
from generate_cover_letter import generate_cover_letter
from extract_text_from_pdf import extract_text_from_pdf
from authenticate_gmail import authenticate_gmail
from constants import *

from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()



llm = ChatGroq(model = "llama-3.3-70b-versatile")

service = authenticate_gmail()

fetch_and_save_json(JOB_LINKS)
filter_jobs(JOB_LISTING, FILTERED_JOBS_PATH)

extract_job_information(llm, FILTERED_JOBS_PATH, JOB_INFORMATION_PATH)

resume = extract_text_from_pdf(llm, RESUME_PATH)

generate_cover_letter(llm, resume, service, JOB_INFORMATION_PATH)


