from auth.routes import authrouter
from templates.routes import templatesrouter
from fastapi import Depends, FastAPI, HTTPException

from database import models, schemas #crud
from database.setup import SessionLocal, engine
from firebase_admin import initialize_app, credentials


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(authrouter)
app.include_router(templatesrouter)

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