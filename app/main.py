from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import List
import psycopg
from psycopg.rows import dict_row  # get teh column names from the database
import time
import models
import schemas
import utils
from database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# while True:
#     try:
#         conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='TestPassword', row_factory=dict_row)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break

#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(3)


@app.get("/")  # path operation decorator
async def root():  # path operation function
    return {"message": "Welcome to my API course"}

# @app.get("/sqlalchemy")
# def test_posts(db:Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}


@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db:Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    return posts

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
    
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
async def create_post(post: schemas.CreatePost, db:Session = Depends(get_db)):
    #   cursor.execute("INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    #   new_post = cursor.fetchone()

    #   conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


"""
@app.get("/posts/{id}")
async def get_post(id: int, response: Response): # anything on the path parameter is a string, fastapi automatically converts it to the type you specify
   # we gotta send the correct response code based on the operation we do, so we use the response object
   if id<200:
     response.status_code = status.HTTP_404_NOT_FOUND
     return{'message':f'Post with id {id} not found'}
      
   return {"post-details": f"Here is the post with id {id}"}

"""

@app.get("/posts/{id}", response_model=schemas.Post)
async def get_post(id: int, db:Session = Depends(get_db)): 
#    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
#    retrieved_post = cursor.fetchone()

   retrieved_post = db.query(models.Post).filter(models.Post.id == id).first()
   
   if not retrieved_post:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
      
   return retrieved_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db:Session = Depends(get_db) ):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
    
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # usually we don't return anything for delete operations


@app.put("/posts/{id}", response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.CreatePost, db:Session = Depends(get_db)): # in put toperations we send all the information along with the infromation that needs to be updated
    # cursor.execute("UPDATE posts SET title= %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    update_post_query = db.query(models.Post).filter(models.Post.id==id)

    post = update_post_query.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
    
    # update_post_query.update({'title':'hey this is my udpated title', 'content':'this is my updated content'}, synchronize_session=False)
    update_post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return update_post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
