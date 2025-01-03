
"""
Why we need schemas?
- Its a pain to get all the values from the body
- the client can send whatever data they want
- the data is not validated
- we want to force the client to send the data in a schema that we expect 

"""
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None  # fully optional field

class CreatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    # class Config:
    #     from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email:EmailStr
    created_at: datetime
