from sqlalchemy import Boolean, Column, ForeignKey, DateTime, String, UUID, JSON, Float, Integer
from sqlalchemy.orm import relationship

from .setup import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    plan = Column(UUID, ForeignKey("plans.id"))
    resumes = relationship("Resume", back_populates="owner")



class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(UUID, primary_key=True, unique=True)
    title = Column(String, unique=True)
    description = Column(String)
    price_in_dollars = Column(Float)
    


class Template(Base):
    __tablename__ = "templates"

    id = Column(UUID, primary_key=True)
    file_url = Column(String, unique=True, index=True)
    image_url = Column(String, index = True)
    date_created = Column(DateTime)
    usage_count = Column(Integer)


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

    id = Column(UUID, primary_key=True)
    owner_id = Column(UUID, ForeignKey("users.id"))
    owner = relationship("User", back_populates="resumes")
    resume = Column(UUID, ForeignKey("templates.id"))

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
    tools = Column(JSON)
    others = Column(JSON)

