from fastapi import APIRouter, Depends
from auth.routes import get_current_user
from database.models import User, Plan
from database.setup import SessionLocal
from utils.response import respond_success
from fastapi.responses import JSONResponse


userrouter = APIRouter(prefix="/user", tags=["user"])

@userrouter.get("/")
async def get_user_details(user: User = Depends(get_current_user)):
    with SessionLocal() as session:
        plan = session.query(Plan).filter_by(id=user.plan_id).first()
        
        session.close()
        return JSONResponse(respond_success({
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "plan": plan.title,
            "is_active": user.is_active,
        }, "User details fetched successfully"))


@userrouter.post("/update")
async def update_user_details(user: User = Depends(get_current_user)):
    return JSONResponse(respond_success(user, "User details updated successfully"))
