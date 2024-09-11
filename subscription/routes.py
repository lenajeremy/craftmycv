from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.setup import SessionLocal
from database.models import Subscription, User, Plan
from database.schemas import SubscriptionCreate
from fastapi.responses import JSONResponse
from utils.response import respond_error, respond_success
from datetime import datetime, timedelta


subscription_router = APIRouter(prefix="/subscription", tags=["subscription"])


@subscription_router.post("/create", response_class=JSONResponse)
def create_subscription(body: SubscriptionCreate):
    with SessionLocal() as session:
        user = session.query(User).filter_by(id=body.user_id).first()
        plan = session.query(Plan).filter_by(id=body.plan_id).first()
        if not user or not plan:
            return JSONResponse(respond_error("User or plan not found"), status_code=404)
        
        # Check if the user has a valid subscription
        current_subscription = session.query(Subscription).filter(
            Subscription.user_id == body.user_id,
            Subscription.end_date > datetime.now()
        ).first()
        
        if current_subscription:
            return JSONResponse(respond_error("User already has a valid subscription"), status_code=400)
        
        subscription = Subscription(user=user, plan=plan, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=plan.duration_in_months * 30))
        session.add(subscription)
        session.commit()
        session.refresh(subscription)
    return respond_success({"subscription_id": str(subscription.id)}, "Subscription created successfully")



@subscription_router.get("/plans/all", response_class=JSONResponse)
def get_all_plans():
    with SessionLocal() as session:
        plans = session.query(Plan).all()
        plans_data = [{
            "id": str(plan.id),
            "title": plan.title,
            "perks": plan.description,
            "duration_in_months": plan.duration_in_months,
            "price_in_dollars": plan.price_in_dollars
        } for plan in plans]
        return JSONResponse(respond_success(plans_data, "Plans fetched successfully"))

