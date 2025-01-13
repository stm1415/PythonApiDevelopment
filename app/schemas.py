
"""
Why we need schemas?
- Its a pain to get all the values from the body
- the client can send whatever data they want
- the data is not validated
- we want to force the client to send the data in a schema that we expect 

"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None  # fully optional field

class CreatePost(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        #orm_mode = True
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        #orm_mode = True
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]