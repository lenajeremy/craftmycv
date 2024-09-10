from auth.routes import authrouter
from templates.routes import templatesrouter
from resumes.routes import resumesrouter
from fastapi import FastAPI
from urllib.parse import unquote

from database import models, schemas #crud
from database.setup import SessionLocal, engine
from firebase_admin import initialize_app, credentials


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(authrouter)
app.include_router(templatesrouter)
app.include_router(resumesrouter)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


cred = credentials.Certificate("craftmycv-2bf02-firebase-adminsdk-jfdby-534ef676e3.json")

firebase_config =  {
  "storageBucket": "craftmycv-2bf02.appspot.com",
}

fb_app = initialize_app(cred, firebase_config)


# session = SessionLocal()
# free_plan = models.Plan(title = "Free Plan", description = "Free forever. Allows you to create only one resume", price_in_dollars = 0)
# session.add(free_plan)
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