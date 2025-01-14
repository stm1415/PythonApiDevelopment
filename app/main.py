from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row  # get teh column names from the database
import app.models
from app.database import engine

from app.routers import post, user, auth, vote

# we no longer need this. This is the command that tells sqlalchemy
# to run the create statements so that it generated all of the tables. Now We are using alembic to manage our database migrations
# app.models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# breakdown of routes in separate file and use them here
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")  # path operation decorator
async def root():  # path operation function
    return {"message": "Welcome to my API course"}

# @app.get("/sqlalchemy")
# def test_posts(db:Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}