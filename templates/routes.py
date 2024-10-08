from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from uuid import uuid4
from database.setup import SessionLocal
from firebase_admin import storage
from database.models import Template, Resume
from datetime import datetime
from utils.response import respond_error, respond_success
from sqlalchemy.exc import NoResultFound
from database import schemas
from auth.routes import  get_current_user
from database.models import User


templatesrouter = APIRouter(prefix="/templates",tags=["templates"])

@templatesrouter.post('/upload', response_class=JSONResponse)
def upload_template(image: UploadFile = File(...), docx_file: UploadFile = File(...), template_name: str = Form(...), template_description: str = Form(...)):
    """
    Endpoint to upload templates
    """
    # Generate a unique template ID
    template_id = str(uuid4())
    session = SessionLocal()

    # Define the Firebase storage paths
    image_path = f"templates/{template_id}/image"
    docx_path = f"templates/{template_id}/file"

    try:
        # Upload image to Firebase Storage
        image_blob = storage.bucket().blob(image_path)
        image_blob.upload_from_file(image.file, content_type=image.content_type)
        image_blob.make_public()
        image_url = image_blob.public_url

        # Upload docx file to Firebase Storage
        docx_blob = storage.bucket().blob(docx_path)
        docx_blob.upload_from_file(docx_file.file, content_type=docx_file.content_type)
        docx_blob.make_public()
        docx_url = docx_blob.public_url

        # Save the template information in the database
        new_template = Template(
            id=template_id,
            name=template_name,
            description=template_description,
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
    finally: 
        session.close()
    


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
    finally:
        session.close()
    # 204 status code implies successful deletion with no content
    return None


