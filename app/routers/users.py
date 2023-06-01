from fastapi import FastAPI, HTTPException, status, Depends, Response, APIRouter
from ..database import engine, get_db
from .. import models, schemas, utils, oath2
from sqlalchemy.orm import session

router = APIRouter(prefix='/users', tags=['Users'])


# the created user/post is going to be stored in user object which is pydantic model. in other words, all fields that we fill in when
# we create a user/post + the added fields by sqlalchemy model which are 'id' and 'created_at' fields are going to be stored in
# 'user'/'post' object as a pydantic model.
# how does sqlalchemy add 'id' and 'created_at' fields? easy! when we create a user/post, we go ahead and call User/Post class
# in models.py, so it's going to create an object of that class, and in that class we have specified the dfault value for 'id' and
# 'created_at' fields.
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: session = Depends(get_db)):
    # hashing the password chosen by user. the user password is accessible by referencing the user object which is a pydantic model.
    user.password = utils.hash(user.password)

    created_user = models.User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user


@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"user with id={id} doesn't exist!")

    return user
