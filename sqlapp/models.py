from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UUID, JSON
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Template(Base):
    __tablename__ = "templates"
    
    id = Column(UUID, primary_key=True)
    file_url = Column(String, unique=True, index=True)
    image_url = Column(String, index = True)


class Resume(Base):
    __tablename__ = "resume"

    """
    Defines a resume.

    - owner details
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
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    email = Column(String)
    phone_number = Column(String)
    role = Column(String)
    description = Column(String)
    experiences = Column(JSON)




class Experience(Base):
    __tablename__ = "experience"

    id = Column(UUID, primary_key=True)
    owner = relationship()