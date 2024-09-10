from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from database import schemas
from database.models import Resume, Template
from database.setup import SessionLocal
from utils.response import respond_error, respond_success

resumesrouter = APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)

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

        new_resume.name = template.name
        new_resume.description = template.description
        new_resume.image_url = template.image_url

        session.add(new_resume)
        session.add(template)

        session.commit()
        session.refresh(new_resume)
        session.refresh(template)
        
        return respond_success({
                "resume_id": str(new_resume.id),
            }, "Resume created successfully")
    except Exception as e:
        return JSONResponse(respond_error(e), status_code=500)
    

@resumesrouter.patch("/{resume_id}/edit", response_class=JSONResponse)
def edit_resume(resume_id: str, request: schemas.ResumeEdit):
    """
    Edit an existing resume --- puts in required fields
    """

    try:
        session = SessionLocal()
        resume= session.query(Resume).filter_by(id=request.id).first()
        print(resume)
        for key, value in request.dict(exclude_unset=True).items():
            setattr(resume, key, value)

        session.commit()


        return respond_success(request.dict(), "Resume edited successfully")
    except Exception as e:
        return JSONResponse(respond_error(e), status_code=500)



@resumesrouter.post("/ai/generate", response_class=JSONResponse)
def generate_resume(request: schemas.Resume):
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