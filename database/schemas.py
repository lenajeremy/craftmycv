from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ItemBase(BaseModel):
    title: str
    description: str #| None : None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode : True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode : True
    



class ResumeBase(BaseModel):
    pass


class ResumeCreate(ResumeBase):
    pass


class Resume(ResumeBase):
    owner_id : str
    template_id : str

    class Config:
        orm_mode : True

class Education(BaseModel):
    id: str
    school: Optional[str] = None
    degree: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    course_studied: Optional[str] = None
    grade: Optional[str] = None

class Experience(BaseModel):
    id: str
    company: Optional[str] = None
    location: Optional[str] = None
    responsibilities: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class ResumeEdit(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None
    experiences: Optional[List[Experience]] = None
    tools: Optional[List[str]] = None
    education: Optional[List[Education]] = None
    others: Optional[dict] = None
    professional_summary: Optional[str] = None
    
    class Config:
        orm_mode = True
