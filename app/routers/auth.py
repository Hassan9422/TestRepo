# in this file, we handle the logic for a user when he wansta log in. we have defined a specific path operation for this matter.
from fastapi import FastAPI, HTTPException, status, Depends, Response, APIRouter
from ..database import engine, get_db
from .. import models, schemas, utils, oath2
from sqlalchemy.orm import session

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login_user(user_credentials: schemas.UserLogin, db: session = Depends(get_db)):
    # first we have to check the database to see whether we have the user or not
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    # if there is no such user: raise an error saying credentials are wrong.
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"wrong credentials")
    # hash the entered password by the client and then compare it with the hashed password inside the database
    # if they are equal, send the token back to the user
    # if not, go ahead and raise an error saying that credentials are wrong
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"wrong credentials")

    # remember, in line below "data" is a dictionary according to the definition of "create_access_token" function in "oauth2.py" file.
    # it can contain multiple things about the user; like "id", "role of the user", "age", etc. but here in this project we have only
    # considered "id" of the user as our payload data + "expiration time" which we have added it into our jwt token by updating it in
    # "create_access_token" function in "oauth2.py" file.
    # with that being said, in line below we have created our jwt token, and finally we return it to the client.
    access_token = oath2.create_access_token(data={"user_id": user.id})
    return {"token": access_token, "token_type": "Bearer"}
