from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from database import schemas
from database.models import Resume, Template
from database.setup import SessionLocal
from utils.response import respond_error, respond_success
from sqlalchemy.exc import SQLAlchemyError
from .utils import upload_file_to_firebase, get_resume_buffer, convert_file_url_to_byes
import io, os, tempfile
from docx2pdf import convert
from pdf2image import convert_from_path


resumesrouter = APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)


@resumesrouter.get('/user/{user_id}', response_class=JSONResponse)
def get_user_resumes(user_id: str):
    """
    Get all resumes for a user
    """
    session = SessionLocal()
    try:
        resumes = session.query(Resume).filter_by(owner_id=user_id).order_by(Resume.updated_at.desc()).all()
        formatted_resumes = [{
            "id": resume.id, 
            "name": resume.name, 
            "created_at": resume.created_at, 
            "updated_at": resume.updated_at
        } for resume in resumes]

        return respond_success(formatted_resumes, "Resumes fetched successfully")
    except SQLAlchemyError as e:
        return JSONResponse(respond_error(str(e)), status_code=500)
    finally:
        session.close()


@resumesrouter.post("/new", response_class=JSONResponse)
def create_resume(request: schemas.Resume):
    """
    Creates a new resume
    """

    try:
        session = SessionLocal()

        new_resume= Resume(
            owner_id = request.owner_id,
            template_id = request.template_id,
        )

        # get template name and description
        template = session.query(Template).filter_by(id=request.template_id).first()
        template.usage_count += 1

        new_resume.description = template.description
        new_resume.image_url = template.image_url

        session.add(new_resume)
        session.add(template)

        session.commit()
        session.refresh(new_resume)
        session.refresh(template)

        return respond_success({
                "resume_id": str(new_resume.id),
                "resume_name": new_resume.name,
            }, "Resume created successfully")
    except Exception as e:
        return JSONResponse(respond_error(e), status_code=500)
    

@resumesrouter.get("/{resume_id}", response_class=JSONResponse)
def get_resume(resume_id: str):
    """
    Get a resume by id
    """

    try:
        session = SessionLocal()
        resume = session.query(Resume).filter_by(id=resume_id).first()

        return respond_success(resume, "Resume fetched successfully")
    except Exception as e:
        return JSONResponse(respond_error(e), status_code=500)


@resumesrouter.patch("/{resume_id}/edit", response_class=JSONResponse)
def edit_resume(resume_id: str, request: schemas.ResumeEdit):
    """
    Edit an existing resume --- puts in required fields
    """

    print(request)

    try:
        session = SessionLocal()
        resume = session.query(Resume).filter_by(id=resume_id).first()

        for key, value in request.dict(exclude_unset=True).items():
            setattr(resume, key, value)

        session.commit()
        session.refresh(resume)

        return respond_success(resume, "Resume edited successfully")
    except Exception as e:
        return JSONResponse(respond_error(e), status_code=500)


@resumesrouter.delete("/{resume_id}/delete", response_class=JSONResponse)
def delete_resume(resume_id: str):
    """
    Delete an existing resume
    """

    try:
        session = SessionLocal()

        resume = session.query(Resume).filter_by(id=resume_id).first()
        template = session.query(Template).filter_by(id=resume.template_id).first()

        template.usage_count -= 1

        session.delete(resume)
        session.commit()
        session.refresh(template)

        return respond_success(None, "Resume deleted successfully")
    except Exception as e:
        return JSONResponse(respond_error(e), status_code=500)

@resumesrouter.post("/{resume_id}/generate", response_class=JSONResponse)
def generate_resume(resume_id: str):
    """
    Generate a resume
    """
    # get resume data
    session = SessionLocal()
    resume = session.query(Resume).filter_by(id=resume_id).first()
    document_bytes = get_resume_buffer(resume_id=resume.id)

    resume_path = f"resumes/{resume.id}/{resume.first_name} {resume.last_name}'s Resume.docx"

    docx_url = upload_file_to_firebase(document_bytes, resume_path)
    resume.docx_url = docx_url

    session.commit()
    session.refresh(resume)

    return respond_success(docx_url, "Resume generated successfully")


@resumesrouter.get("/{resume_id}/preview", response_class=JSONResponse)
async def preview_resume(resume_id: str):
    session = SessionLocal()
    resume = session.query(Resume).filter_by(id=resume_id).first()

    if resume is None:
        return JSONResponse(respond_error(f"Resume with ID: {resume_id} not found"), status_code=404)
    
    if resume.docx_url or resume.docx_url == "":
        document_bytes = get_resume_buffer(resume_id=resume.id)
        resume_path = f"resumes/{resume.id}/{resume.first_name} {resume.last_name}'s Resume.docx"
        docx_url = upload_file_to_firebase(document_bytes, resume_path)
        resume.docx_url = docx_url

    # pdf_url = resume.pdf_url

    # if pdf_url is None or pdf_url == "":
    #     import requests
    #     print("generating pdf from docx")
    #     res = requests.post(url='https://api.pdf.co/v1/pdf/convert/from/doc', data={
    #         "url": docx_url, 
    #         "name": f"{resume.first_name} {resume.last_name}'s Resume.pdf", 
    #         "async": False
    #     }, headers={"X-Api-Key": os.environ["PDFCO_API_KEY"]})

    #     if res.status_code == 200:
    #         res_json = res.json()
    #         pdf_url = res_json['url']
    #         pdf_bytes = convert_file_url_to_byes(pdf_url)
    #         pdf_url = upload_file_to_firebase(pdf_bytes, f"resumes/{resume.id}/{resume.first_name} {resume.last_name}'s Resume.pdf", file_type="application/pdf")
    #         resume.pdf_url = pdf_url
    #     else:
    #         return respond_error(res.json())
    

    # with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
    #     pdf_bytes = convert_file_url_to_byes(pdf_url)
    #     temp_pdf.write(pdf_bytes.getvalue())
    #     pdf_url = temp_pdf.name

    # images = convert_from_path(pdf_url)
    # img_byte_arr = io.BytesIO()
    # images[0].save(img_byte_arr, format='PNG')
    # img_byte_arr.seek(0)

    # image_url = upload_file_to_firebase(img_byte_arr, f"resumes/{resume.id}/{resume.first_name} {resume.last_name}'s Resume.png",file_type="image/png")
    # resume.image_url = image_url

    # # clean up temporary files
    # os.remove(pdf_url)
    preview_url = f"https://view.officeapps.live.com/op/view.aspx?src={docx_url}"

    session.commit()
    session.refresh(resume)

    return respond_success({"resume_image_url": preview_url}, "Retrieved resume image")
    

@resumesrouter.post("/ai/generate", response_class=JSONResponse)
def generate_resume_ai(request: schemas.Resume):
    # request.field  = 'profile_summary'
    # request.field = 'workexperience_summary'
    # request.field = 'education_summary'
    # request.field = 'skills_summary'
    # request.field = 'certifications_summary'
    # request.field = 'languages_summary'
    # request.field = 'interests_summary'
    # request.field = 'achievements_summary'
    # request.field = 'projects_summary'
    # request.field = 'publications_summary'
    # request.field = 'honors_summary'

    prompts = {
        "profile_summary": "Create a profile summary for the resume for a {request.role} in {request.industry} with the following skills: {requst.skillsdetails}",
        "workexperience_summary": "Create a work experience summary for the resume",
        "education_summary": "Create a education summary for the resume",
        "skills_summary": "Create a skills summary for the resume",
        "certifications_summary": "Create a certifications summary for the resume",
        "languages_summary": "Create a languages summary for the resume",
        "interests_summary": "Create a interests summary for the resume",
        "achievements_summary": "Create a achievements summary for the resume",
        "projects_summary": "Create a projects summary for the resume",
    }

    # get data from frontend
    # generate prompt
    # send to openai
    # get response
    # return response

    return respond_success(request.dict(), "Resume generated successfully")

