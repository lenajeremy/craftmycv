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

class Experience(BaseModel):
    company: str
    work_done: str
    start_date: str
    end_date: str

class Education(BaseModel):
    school: str
    degree: str
    start_date: str
    end_date: str
    description: Optional[str] = None

class ResumeEdit(BaseModel):
    owner_id: Optional[str] = None
    template_id: Optional[str] = None
    download_count: Optional[int] = None
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

    class Config:
        orm_mode = True

class Experience(BaseModel):
    company: str
    work_done: str
    start_date: str
    end_date: str