from extract_job_information import extract_job_information
from load_job_listing import fetch_and_save_json
from generate_cover_letter import generate_cover_letter
from extract_text_from_pdf import extract_text_from_pdf
from authenticate_gmail import authenticate_gmail

from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

job_links = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/a8f199d8b27e7ffa6a6aebce8908e6f7e53c00ed/.github/scripts/listings.json"

llm = ChatGroq(model = "llama-3.3-70b-versatile")

service = authenticate_gmail()

# fetch_and_save_json(job_links)
# extract_job_information(llm)

resume = extract_text_from_pdf(llm, "Supraja_Srikanth_Resume.pdf")

generate_cover_letter(llm, resume, service)


