# in this file we are going to handle all the logic for creating and setting up different parts of a JWT token
from fastapi import FastAPI, HTTPException, status, Depends, Response, APIRouter
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import session
from .config import setting
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer

# line below is very important. this line basically is saying that I'm gonna get the token from the "login" path operation! it basically
# ties everything together, and now we can pass this token grabbed from "login" route when he logged in, and now we can pass it to any
# of our functions in this file.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes


# in function below, "data" is the payload that we wanna send with jwt token. basically we wanna encode this payload into our
# jwt token.
def create_access_token(data: dict):
    # because we don't wanna mess with the original payload of the token, we are going to make a copy of the payload and then
    # making changes in it and finally encoding it into our jwt token.
    # remember, "data" is a dictionary. it can contain multiple things about the user; like "id", "role of the user", "age",
    # etc. but here in this project we have only considered "id" as our payload data + "expiration time"
    to_encode = data.copy()
    # now we are going to create "expiration" field in our payload before encoding the payload into our jwt token:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # and now we add the "expiration" field in our payload by updating our payload data which is "to_encode"
    to_encode.update({"exp": expire})
    # now that we have added and encoded desired fields in payload (first, "data" as a dictionary which can be everything like the
    # id of the user, etc. and second the "expiration field"), finally in line below we can create our jwt token having three pieces
    # of information; "payload", "algorithm type" and "secret key".
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# in the previous function, we created and sent the jwt token to the user. now the user wants to get a resource or endpoint that
# needs him to be logged in. so he needs to send his token data alongside with other data, so that our API can verify whether
# the token is valid or not. in function below we have defined the logic for verifying a jwt token.
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")

        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


# function below is going to be passed as an argument to any of our path operations as a dependency. so whenever the user is trying
# to login, our API is going to take the jwt token sent by the user, verify it by calling the "verify_access_token" function
# and extract the "id" from payload, and then if we want we can fetch the corresponding user from the database and use it as an
# argument in the path operation function.
# the purpose of having below function is that we can get the logged-in user and pass it to any of our path operation.
# remember now before having current version of below function, we were returning 'token_data' which is 'id' of the user. we could
# pass that 'id' and pass it to our path operations, and each of our path operations could fetch the user from the database
# themselves having this 'id' returned from function below.  but what we can do is that, instead of passing this 'id' to each of our
# path operations and then fetching the user inside of the path operations, we can simply fetch the user here in below function and
# then passing it to our path operations so that our path operations don't have to fetch the user from database, because we pass the
# user directly to them.
# remember in current version of function below, because we are going to fetch the user from database, we need database dependencies.
def get_current_user(token: str = Depends(oauth2_scheme), db: session = Depends(database.get_db)):
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not Authorized! You have to Login first!",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user


