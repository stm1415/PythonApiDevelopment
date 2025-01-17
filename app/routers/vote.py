from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, oauth2, database

router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==current_user.id)
    found_vote = vote_query.first()
    if (vote.dir ==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f" User {current_user.id} has already upvoted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added a vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {current_user.id} has not voted on post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully removed the vote"}
