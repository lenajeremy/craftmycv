"""
Utils for resume creation
"""
from io import BytesIO
from datetime import datetime
import requests
from typing import List
from docxtpl import DocxTemplate
from firebase_admin import storage
from database.models import Resume, Template
from database.setup import SessionLocal


def convert_file_url_to_byes(url: str) -> BytesIO:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        docx_buffer = BytesIO(response.content)
        return docx_buffer
    else:
        return None


def get_resume_buffer(resume_id: str):
    """
    Returns a buffer array with the generated resume (in docx)
    """
    with SessionLocal() as session:
        resume = session.query(Resume).filter_by(id=resume_id).first()
        template = session.query(Template).filter_by(id=resume.template_id).first()
        
        docx_buffer = convert_file_url_to_byes(url=template.file_url)
        document = DocxTemplate(docx_buffer)
        resume_data = generate_resume_data(resume)
        print(resume_data)
        
        document.render(resume_data)

        document_bytes = BytesIO()
        
        document.save(document_bytes)

        return document_bytes

def format_date(date_str: str) -> str:
    date = datetime.fromisoformat(date_str)
    return date.strftime("%B %d, %Y")

def replace_datekeys(d: dict, keys: List[str]) -> dict:
    for key in keys:
        d[key] = format_date(d[key])
    return d


def generate_resume_data(resume: Resume):
    return {
        "full_name": f"{resume.first_name} {resume.last_name}".title(),
        "phone_number": resume.phone_number,
        "email_address": resume.email,
        "address": resume.address,
        "link": "https://google.com",
        "profile_summary": resume.professional_summary,
        "education": [replace_datekeys(edu, ["start_date", "end_date"]) for edu in resume.education],
        "experience": [replace_datekeys(exp, ["start_date", "end_date"]) for exp in resume.experiences],
        "skills": resume.skills
    }


def upload_file_to_firebase(file: BytesIO, file_path: str, file_type: str = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"):
    file.seek(0)

    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    blob.upload_from_file(file, content_type=file_type)

    blob.make_public()
    return blob.public_url