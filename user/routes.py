from fastapi import APIRouter, Depends
from auth.routes import get_current_user
from database.models import User, Plan
from database.setup import SessionLocal
from utils.response import respond_success
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from sqlalchemy import and_
from database.models import Subscription


userrouter = APIRouter(prefix="/user", tags=["user"])

@userrouter.get("/")
async def get_user_details(user: User = Depends(get_current_user)):
    with SessionLocal() as session:
        active_subscription = session.query(Subscription).filter(
            and_(
                Subscription.user_id == user.id,
                Subscription.end_date > datetime.now(timezone.utc)
            )
        ).first()
        free_plan = session.query(Plan).filter(Plan.title.ilike("%free%")).first()

        if active_subscription:
            plan: Plan | None = active_subscription.plan
        else:
            plan = free_plan
        
        res = {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "plan": plan.title,
            "has_valid_subscription": active_subscription is not None,
            "is_active": user.is_active,
        }

        return JSONResponse(respond_success(res, "User details fetched successfully"))


@userrouter.post("/update")
async def update_user_details(user: User = Depends(get_current_user)):
    return JSONResponse(respond_success(user, "User details updated successfully"))
