from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from uuid import uuid4
from database.setup import SessionLocal
from firebase_admin import storage
from database.models import Template, Resume
from datetime import datetime
from utils.response import respond_error, respond_success
from sqlalchemy.exc import NoResultFound
from database import schemas


templatesrouter = APIRouter(prefix="/templates",tags=["templates"])

@templatesrouter.post('/upload', response_class=JSONResponse)
def upload_template(image: UploadFile = File(...), docx_file: UploadFile = File(...)):
    """
    Endpoint to upload templates
    """
    # Generate a unique template ID
    template_id = str(uuid4())
    session = SessionLocal()

    # Define the Firebase storage paths
    image_path = f"{template_id}/{image.filename}"
    docx_path = f"{template_id}/{docx_file.filename}"

    try:
        # Upload image to Firebase Storage
        image_blob = storage.bucket().blob(image_path)
        image_blob.upload_from_file(image.file, content_type=image.content_type)
        image_url = image_blob.public_url

        # Upload docx file to Firebase Storage
        docx_blob = storage.bucket().blob(docx_path)
        docx_blob.upload_from_file(docx_file.file, content_type=docx_file.content_type)
        docx_url = docx_blob.public_url

        # Save the template information in the database
        new_template = Template(
            id=template_id,
            file_url=docx_url,
            image_url=image_url,
            date_created=datetime.now(),
            usage_count=0
        )
        session.add(new_template)
        session.commit()
        session.refresh(new_template)

        return respond_success({
            "template_id": new_template.id,
            "image_url": image_url,
            "file_url": docx_url
        }, "Template uploaded successfully")
    except Exception as e:
        print(e)
        return respond_error("Failed to upload template")
    


@templatesrouter.get("/all", response_class=JSONResponse)
def get_all_templates(page: int = Query(1, description="Page number, starting from 1", ge=1), pageCount: int = Query(10, description="Number of templates per page", ge=1)):
    """
    Endpoint to list all available teplates
    """
    offset = (page - 1) * pageCount

    try:
        with SessionLocal() as session:
            total_templates = session.query(Template).count()
            total_pages = (total_templates + pageCount - 1) // pageCount

            if offset >= total_templates and total_templates != 0:
                return JSONResponse(respond_error("Page out of range"), status_code=404)
            
            templates = session.query(Template).offset(offset).limit(pageCount).all()
        return respond_success({
            "total_templates": total_templates,
            "total_pages": total_pages,
            "current_page": page,
            "templates": templates
        }, "Successfully retrieved templates")
    except Exception as e:
        print(e)
        return JSONResponse(respond_error("Internal server error"), status_code=500)
    

@templatesrouter.delete("/{template_id}", status_code=204)
def delete_template(template_id: str):
    """
    Endpoint to delete a template by its ID.
    """

    session = SessionLocal()
    try:
        # Query the template by ID
        template = session.query(Template).filter_by(id=template_id).one()

        # Delete the template
        session.delete(template)
        session.commit()
        
    except NoResultFound:
        # Raise a 404 error if the template does not exist
        raise HTTPException(status_code=404, detail="Template not found")
    
    # 204 status code implies successful deletion with no content
    return None


@templatesrouter.post("/resume/create", response_class=JSONResponse)
def create_resume(request: schemas.Resume):
    """
    Create a resume
    """

    try:
        session = SessionLocal()

        new_resume= Resume(
            owner_id = request.owner_id,
            template_id = request.template_id
        )
        
        session.add(new_resume)
        session.commit()
        session.refresh(new_resume)

        return respond_success({
                "resume_id": str(new_resume.id),
            }, "Resume created successfully")
    except Exception as e:
        return JSONResponse(respond_error(e), status_code=500)
    

@templatesrouter.patch("/resume/edit", response_class=JSONResponse)
def edit_resume(request: schemas.ResumeEdit):
    """
    Edit a resume
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