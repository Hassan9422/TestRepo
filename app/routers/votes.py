from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, Depends, Response, APIRouter
from ..database import engine, get_db
from .. import models, schemas, utils, oath2
from sqlalchemy.orm import session

router = APIRouter(prefix='/vote', tags=['Votes'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote1(vote: schemas.Vote, db: session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    # first I have to check whether the requested post to be liked exists or not:
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"the post with id={vote.post_id} does not exist!")

    # now I have to check whether the same user has voted for the same post or not? because we wanna check the existence of vote on the
    # requested post; so we are going to check the "vote" table. first the post_id has to be thesame post_id requested by the user and second
    # the user_id should be the same as user_id retrieved from token:
    found_vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    if vote.dir is True:
        if found_vote_query.first():
            raise HTTPException(status.HTTP_409_CONFLICT, detail=f"post with id={vote.post_id} has been voted already by user with id="
                                                                 f"{current_user.id}")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return "you voted on the post successfully!"

    else:
        if not found_vote_query.first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id={vote.post_id} has NOT been voted already by you! there is no "
                                                                  f"vote to remove here!")
        found_vote_query.delete(synchronize_session=False)
        db.commit()
        return "You successfully deleted the post!"
