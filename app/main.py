from fastapi import FastAPI, HTTPException, status, Depends, Response
from fastapi.params import Body
import psycopg2
# allowing users from different domains on the web browser to access our API which currently is running on "localhost:8000"
from fastapi.middleware.cors import CORSMiddleware

# in psycopg2 library, we need to import this, because the way that this library works is that when we make a query
# to a database to retrieve a bunch of row from database, it doesn't include the column names! it just returns the
# rows values without column names! so we can not know which row is for which column. to abstain from that we need to
# import this extra thing below from this library.
from psycopg2.extras import RealDictCursor
from app import models, schemas, utils
from app.database import engine, get_db
from app.routers import users, posts, auth, votes

app = FastAPI()
# allowing every domain on a web browser to talk to our API:
origins = ["*"]
# remember you can limit the allowed methods ot headers, so that users can't use for example "put" or "delete" requests. you can limit them to
# only use "get" method.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# in the second method of interacting with the database withing fastapi, we had to use sqlalchemy to create all the tables, and also
# we had to just use python commands to send queries to database. if your remember, we have created a connection to our database in
# "database.py" already in this method; and also we created all of our tables as python classes in "models.py" file. but according
# to the fastapi documentation on how to work with sqlalchemy, if we wanna create all tables that we have defined in "models.py",
# we need to add line below in our main file which is here:
models.Base.metadata.create_all(bind=engine)

'''
# the reason that we have created this while loop is that we wanna make sure that we have connected to our databas
# then we break out of the loop. if we don't connect to the database, we have to try again until we connect to the
# database successfully.
while True:
    try:
        # again, what cursor_factory does in below is that it goves you the column name as well as the value of rows,
        # so you can know what column is mapped to what row and data and it returns you a nice little python dictionary
        # of columns.
        conn = psycopg2.connect(host='localhost', database='FastAPI_2', user='postgres', password='940202',
                                cursor_factory=RealDictCursor)
        # we are going to use below object to make queries to our database later in our path operation sections.
        cursor = conn.cursor()
        print('connection was successful')
        break
    # if we couldn't connect to database:
    except Exception as error:
        print('connecting to database was not successful')
        print('error is: ', error)

'''

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get('/get')
def root():
    return {'message': 'this is your first request!'}


# what is this Body here? so it comes from fastapi library, and we have to use it if we wanna extract/retrieve the
# data which we have sent to the API from Postman. and remember, most people use JSON data format when they wanna
# send a post request to an API. JSON data is very similar to a python dictionary. and notice that how we have
# converted the json data extracted from the Body of the post request to a python dictionary below. because we wanna
# grab and use that data in our function.
"""
@app.post('/create')
def root(payload: dict = Body(...)):
    return {'message': f"{payload['title']}", 'content': f"{payload['content']}"}
"""


# here we can reference Post pydantic model and save it in a variable called post. our purpose is to validate the
# data now we don't have to use Body to extract the data from frontend! because we use pydantic model, and it will
# automatically retrieve the data and check the validity of it. so keep in mind that 'Post' is a pydantic model and
# 'post' is variable that we want to store our pydantic model in. we can convert the 'post' from a pydantic model to
# a python dictionary using dict() method
@app.post('/create')
# keep in mind that 'Post' is our schema in the pydantic model and 'post' is variable that we want to store our
# schema/pydantic model in.
def root(post: schemas.PostCreate):
    print(post)
    # keep in mind that you can access any property based off of schema you have defined, like below
    print(post.published)
    # we can also convert the 'post' from a pydantic model to a python dictionary using dict() method
    print(post.dict())
    return post
