from pydantic import BaseModel, EmailStr

class PersonBase(BaseModel):
    gender: str
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    location: str

class PersonCreate(PersonBase):
    pass

class PersonResponse(PersonBase):
    id: int

    class Config:
        from_attributes = True