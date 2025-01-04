from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import List
import psycopg
from psycopg.rows import dict_row  # get teh column names from the database
import app.models
from app.database import engine, get_db
from sqlalchemy.orm import Session

from app.routers import post, user

app.models.Base.metadata.create_all(bind=engine)

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

# breakdown of routes in separate file and use them here
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")  # path operation decorator
async def root():  # path operation function
    return {"message": "Welcome to my API course"}

# @app.get("/sqlalchemy")
# def test_posts(db:Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}