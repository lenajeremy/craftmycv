from pydantic import BaseModel


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

class ResumeEdit(ResumeBase):
    id : str
    download_count : int
    first_name : str
    last_name : str
    address : str
    email : str
    phone_number : str
    role : str
    description : str
    experiences : str # was Column(JSON)
    tools : str # was Column(JSON)
    others : str# was Column(JSON)

    class Config:
        orm_mode : True