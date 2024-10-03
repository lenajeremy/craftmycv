"""
Subscription Routes
Created by Jeremiah Lena
"""
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from database.setup import SessionLocal
from database.models import Subscription, User, Plan
from database.schemas import SubscriptionCreate
from utils.response import respond_error, respond_success


subscription_router = APIRouter(prefix="/subscription", tags=["subscription"])


@subscription_router.post("/create", response_class=JSONResponse)
def create_subscription(body: SubscriptionCreate):
    """
    Creates a new subscription for a user
    """
    with SessionLocal() as session:
        user = session.query(User).filter_by(id=body.user_id).first()
        plan = session.query(Plan).filter_by(id=body.plan_id).first()
        if not user or not plan:
            return JSONResponse(respond_error("User or plan not found"), status_code=404)
        if plan.title.lower().find("free") != -1:
            return JSONResponse(respond_error("Cannot subscribe to Free plan"), status_code=400)
        
        # Check if the user has a valid subscription
        current_subscription = session.query(Subscription).filter(
            Subscription.user_id == body.user_id,
            Subscription.end_date > datetime.now(timezone.utc)
        ).first()
        
        if current_subscription:
            return JSONResponse(respond_error("User already has a valid subscription"), status_code=400)
        
        subscription = Subscription(user=user, plan=plan, start_date=datetime.now(timezone.utc), end_date=datetime.now(timezone.utc) + timedelta(days=plan.duration_in_months * 30))
        session.add(subscription)
        session.commit()
        session.refresh(subscription)
    return respond_success({"subscription_id": str(subscription.id)}, "Subscription created successfully")



@subscription_router.get("/plans/all", response_class=JSONResponse)
def get_all_plans():
    """
    List all available plans
    """
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

