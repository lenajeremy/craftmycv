from auth.routes import authrouter
from subscription.routes import subscription_router
from templates.routes import templatesrouter
from resumes.routes import resumesrouter
from user.routes import userrouter
from fastapi import FastAPI
from mails.send_mail import send_mail
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from database import models, schemas #crud
from database.setup import SessionLocal, engine
from firebase_admin import initialize_app, credentials



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(authrouter)
app.include_router(subscription_router)
app.include_router(templatesrouter)
app.include_router(resumesrouter)
app.include_router(userrouter)

app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name = "index.html")



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import os, json
cred_json = os.getenv("FIREBASE_CERTIFICATE")
cred_dict = json.loads(cred_json)

cred = credentials.Certificate(cred_dict)

firebase_config =  {
  "storageBucket": "craftmycv-2bf02.appspot.com",
}

fb_app = initialize_app(cred, firebase_config)

# session = SessionLocal()
free_plan = models.Plan(
    title = "Free Plan", 
    description = [
        "Access to a limited selection of simple, professional resume templates.",
        "Create and save up to 1 resume.",
        "Generate professional summaries and job descriptions using basic AI-powered suggestions.",
        "Export resumes as a PDF.",
    ],
    duration_in_months = 999999,
    price_in_dollars = 0
)

pro_plan = models.Plan(
    title = "Pro Plan",
    description = [
        "Access to a broader selection of modern and industry-specific templates.",
        "Create, save, and manage up to 5 resumes.",
        "AI-powered suggestions for bullet points, skills, and professional summaries tailored to specific industries.",
        "Export resumes in PDF, Word, and TXT formats.",
    ],
    duration_in_months = 1,
    price_in_dollars = 9.99
)

premium_plan = models.Plan(
    title = "Premium Plan",
    description = [
        "Unlimited access to all premium templates, including exclusive designs.",
        "Advanced AI to fully optimize resumes, including tailored content, keyword optimization, and industry-specific guidance.",
        "Access insights on resume views, downloads, and keyword match rates.",
        "Create and customize cover letters, portfolios, and LinkedIn profile optimization.",
    ],
    duration_in_months = 12,
    price_in_dollars = 99.99
)

# session.add(free_plan)
# session.add(pro_plan)
# session.add(premium_plan)
# session.commit()

# from firebase_admin import storage

# # get all the templates
# session = SessionLocal()
# bucket = storage.bucket()
# templates = session.query(models.Template).all()
# for template in templates:
#     file_name = unquote(template.file_url.split('/')[-1])
#     image_file_name = unquote(template.image_url.split('/')[-1])

#     image_blob = bucket.blob(f"{template.id}/{image_file_name}")
#     file_blob = bucket.blob(f"{template.id}/{file_name}")
#     image_blob.metadata = {"public": True}
#     file_blob.metadata = {"public": True}
#     image_blob.make_public()
#     file_blob.make_public()
#     image_blob.update()
#     file_blob.update()

#     template.file_url = file_blob.public_url
#     template.image_url = image_blob.public_url
#     session.commit()