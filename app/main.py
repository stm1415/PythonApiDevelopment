from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

import schemas

app = FastAPI()

@app.get("/")  # path operation decorator
async def root():  # path operation function
    return {"message": "Welcome to my API course"}

@app.get("/posts")
async def get_posts():
    return {"data": "Here are all your posts"}

"""

# @app.post("/createposts")
# async def create_post(payload: dict = Body(...)):  # extract all the fields from the body, convert into a python dictionary and store in the variable payload
#    return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}
@app.post("/createposts")
async def create_post(payload: schemas.Post):
      print(payload)    # title='Top beaches in Nepal' content='Checkout these recommendations here.' published=False rating=9
      payload_dict = payload.dict()
      print(payload_dict) # {'title': 'Top beaches in Nepal', 'content': 'Checkout these recommendations here.', 'published': False, 'rating': 9}
      #return {"new_post": f"title_: {payload.title}, content_: {payload.content}, rating: {payload.rating}"}
      return {"data": payload_dict}

"""
    
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.Post):
      #post.dict()
      return {"data": post}


"""
@app.get("/posts/{id}")
async def get_post(id: int, response: Response): # anything on the path parameter is a string, fastapi automatically converts it to the type you specify
   # we gotta send the correct response code based on the operation we do, so we use the response object
   if id<200:
     response.status_code = status.HTTP_404_NOT_FOUND
     return{'message':f'Post with id {id} not found'}
      
   return {"post-details": f"Here is the post with id {id}"}

"""

@app.get("/posts/{id}")
async def get_post(id: int): # anything on the path parameter is a string, fastapi automatically converts it to the type you specify
   # we gotta send the correct response code based on the operation we do, so we use the response object
   if id<200:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
      
   return {"post-details": f"Here is the post with id {id}"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    if id<200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # usually we don't return anything for delete operations


@app.put("/posts/{id}")
async def update_post(id: int, post: schemas.Post): # in put toperations we send all the information along with the infromation that needs to be updated 
    if id<200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
    return {"data": f"Post with id {id} has been updated with these values: {post}"}