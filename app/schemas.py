
"""
Why we need schemas?
- Its a pain to get all the values from the body
- the client can send whatever data they want
- the data is not validated
- we want to force the client to send the data in a schema that we expect 

"""
from typing import Optional
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None  # fully optional field