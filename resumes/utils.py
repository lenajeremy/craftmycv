import requests
from firebase_admin import storage
from io import BytesIO
from database.models import Resume
from database.schemas import ResumeEdit


def get_templates_byes_from_url(url: str) -> BytesIO:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        docx_buffer = BytesIO(response.content)
        return docx_buffer
    else:
        return None


def generate_resume_data(resume: Resume):
    return {
        "full_name": f"{resume.first_name} {resume.last_name}".title(),
        "phone_number": resume.phone_number,
        "email_address": resume.email,
        "address": resume.address,
        "link": "https://google.com",
        "profile_summary": resume.professional_summary,
        "education": resume.education,
        "experience": resume.experiences,
        "skills": resume.skills
    }


def upload_file_to_firebase(file: BytesIO, resume_id: str):
    file.seek(0)

    bucket = storage.bucket()
    blob = bucket.blob(f"resumes/{resume_id}.docx")
    blob.upload_from_file(file, content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    blob.make_public()
    return blob.public_url