"""Database models for the application."""
from uuid import uuid4
import random
import string

from sqlalchemy import Boolean, Column, ForeignKey, DateTime, String, UUID, JSON, Float, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import ChoiceType

from .setup import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, unique=True, default=uuid4)
    name = Column(String, default="")
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    plan_id = Column(UUID, ForeignKey("plans.id"))
    plan = relationship("Plan", back_populates="users")
    resumes = relationship("Resume", back_populates="owner")
    auth_sessions = relationship("AuthSession", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")


def random_session_key():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(16))


class AuthSession(Base):

    SESSION_TYPES = [
        ("email_login", "Email Login Session"),
        ("email_validation", "Email Validation Session"),
        ("password_reset", "Reset Password Session")
    ]

    __tablename__ = "auth_sessions"
    id = Column(UUID, primary_key=True, unique=True, default=uuid4)
    user = relationship("User", back_populates="auth_sessions")
    user_id = Column(UUID, ForeignKey("users.id"))
    key = Column(String, nullable=False, default=random_session_key)
    type = Column(ChoiceType(SESSION_TYPES))


class Plan(Base):
    __tablename__ = "plans"

    id = Column(UUID, primary_key=True, unique=True, default=uuid4)
    title = Column(String, unique=True)
    description = Column(JSON, default=[])
    duration_in_months = Column(Integer)
    price_in_dollars = Column(Float)
    users = relationship("User", back_populates="plan")
    subscriptions = relationship("Subscription", back_populates="plan")
    
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID, primary_key=True, unique=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"))
    plan_id = Column(UUID, ForeignKey("plans.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
    

class Template(Base):
    __tablename__ = "templates"

    id = Column(UUID, primary_key=True, default=uuid4)
    file_url = Column(String, unique=True, index=True)
    image_url = Column(String, index = True)
    name = Column(String)
    description = Column(String)
    date_created = Column(DateTime)
    usage_count = Column(Integer)
    resumes= relationship('Resume', back_populates='template')


class Resume(Base):
    __tablename__ = "resumes"

    """
    Defines a resume.

    - owner details
        - template
        - owner
        - download_count
        - first name
        - last name
        - address
        - email
        - phone number
        - role
        - description
        - experiences[
            - company
            - work done (string[] | string)
            - time start (Date)
            - time end (Data | present)
        ]
        - tools string[]
        - others: dictionary{
            string: string | string[]
        }
    """

    id = Column(UUID, primary_key=True, default=uuid4)
    owner_id = Column(UUID, ForeignKey("users.id"))
    owner = relationship("User", back_populates="resumes")
    template = relationship("Template", back_populates="resumes")
    template_id = Column(UUID, ForeignKey("templates.id"))
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    name = Column(String, default="Untitled Resume")
    docx_url = Column(String, default="")
    pdf_url = Column(String, default="")
    image_url = Column(String, default="")
    last_preview_date = Column(DateTime, nullable=True)
    last_download_date = Column(DateTime, nullable=True)
    resume_data_updated_at = Column(DateTime, nullable=False, default=func.now())
    


    download_count = Column(Integer, default=0)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    email = Column(String)
    phone_number = Column(String)
    role = Column(String)
    description = Column(String)
    """
    Experiences should follow the following schema
    {
        "company": string,
        "work_done": string || string[],
        "start_date": Date,
        "end_date": Date || "present"
    }
    """
    experiences = Column(JSON)
    skills = Column(JSON)
    others = Column(JSON)
    education = Column(JSON)
    professional_summary = Column(String)




