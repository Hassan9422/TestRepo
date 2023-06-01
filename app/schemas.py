from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

'''
# this is a pydantic model we are gonna define to validate the data that frontend sends to the API. Basemodel has
# extended this class to be a pydantic model to validate frontend data.
class Post(BaseModel):
    title: str
    content: str
    # we can set a default value for our property in a case that frontend doesn't provide any value for it
    published: bool = True
    # however, we can make our property completely optional, setting the default value of our property as 'None':
    # rating: Optional[int] = None
'''


class PostBase(BaseModel):
    title: str
    content: str
    # we can set a default value for our property in a case that frontend doesn't provide any value for it
    published: bool = True
    # however, we can make our property completely optional, setting the default value of our property as 'None':
    # rating: Optional[int] = None


# the reason that we wanna define separate schemas for each of the requests( for example one schema for creating a request(a
# post http request) and one separate schema for updating a post ( a put http request) ) is that it's likely that we are not going
# to allow the user to update all the fields of the existed post, and we wanna limit the user to just change one of the fields of
# the existing post. that is why it is rational to have different separate schemas for each different type of http request.
class PostCreate(PostBase):
    pass


# keep in mind that we have defined these response models and as they are pydantic models, they take dicts as their input. keep in
# mind that the response models here take the returned value of path operations as input and perform the validation process on that.
# and we know that since we use sqlalchemy, the returned value of different path operations is a sqlalchemy model and to
# make our response model accept this sqlalchemy model, we added Config class like below.
# also remember that, when we create a post or a user, we fill required fields according to the schema and send it to desired API
# endpoint. and then our  sqlalchemy model automatically adds 'id' and 'created_at' fields for each post or user that we create.
# so keep in mind that each created post/user in our database has more fields than the fields we fill in when we create them. and they
# are 'id' and 'created-at' fields created by the sqlalchemy model itself.
class UserResponse(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr

    class Config:
        orm_mode = True


# we could add "owner_id" in PostCreate table, so in that way the user has to provide his "id" when he wanna create a post. but we don't wanna
# exactly do that. instead we want to retrieve the "id" of the user from the jwt token when he logs in. the user doesn't need to enter his
# email every time he wanna grab something. it's going to be done by the jwt token.
# what we wanna do is that we are going to return the id of the user back to him. so we have to add "id" here in below pydantic model which is
# for returning the post to the user.
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    # pydantic model only works with a dictionary. it takes a dict and converts it to pydantic model. but when we for example create a
    # post, we try to send back a sqlalchemy model to the user not a dict that pydantic can work with. so, in this case,
    # we have to think of a way to solve this issue. we can solve it by adding class below. it goes ahead and tells pydantic model
    # to take the data even if it is an orm model, like when we create a post and send it back to the user as was explained.
    class Config:
        orm_mode = True


class PostVote(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# the reason that we have defined a pydantic model for jwt token is that when the user is trying to send the token to API,
# we have to make sure that it follows the correct format.
# remember, whenever the user is trying to send some type of data into our API, we usually need to define a pydantic model for that
# data to check the validity of the data. here the user is trying to send his jwt token to API so that API can check the validity of
# the token. so here we can define a pydantic model for the token that user sends to API.
class Token(BaseModel):
    token: str
    token_type: str


# Here we can provide a pydantic model for our payload data that we have embedded in our JWT token. as you know, we decided to only
# embed "id" of the user in payload data.
class TokenData(BaseModel):
    id: Optional[int] = None


# class below make sure that the user provides the correct info when he is going to create a vote on a specific post. we don't need to send
# the user id in the body, we can retrieve it from jwt token.
class Vote(BaseModel):
    post_id: int
    dir: bool
