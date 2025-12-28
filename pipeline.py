from send_cv import send_cv
from load_job_listing import fetch_and_save_json, filter_jobs
from extract_text_from_pdf import extract_text_from_pdf
from authenticate_gmail import authenticate_gmail
from constants import *

from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model = "llama-3.3-70b-versatile")

service = authenticate_gmail()

fetch_and_save_json(JOB_LINKS)

resume = extract_text_from_pdf(llm, RESUME_PATH)

send_cv(llm, JOB_LISTING, resume, service)

