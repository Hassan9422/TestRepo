# this is a file in which we have gathered all logic for initialization of a database.
# this file is going to handle our database connection. we have defined the logic for creating the tables as python classes in
# another file in current directory in "models.py". so this file is only for handling the connection to the database.
# please have a look at sqlalchemy section in fastapi documentation here https://fastapi.tiangolo.com/tutorial/sql-databases/
# it has explained in details that what should we import and how we can establish a connection to our database and how we should
# define our tables etc.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting

# first of all we should tell fastapi where is our postgres database located? if you remember, in previous method that we used to
# connect to the database using psycopg2, we used psycopg2, and we specified username, password etc. of the database.
# here we will do the same thing but this time we use sqlalchemy.
# according to the fastapi documentation, we can do it like below:

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}/{setting.database_name}"

# According to documentation, we need to create an engine, this engine is responsible for making the connection between sqlalchemy
# and the database. according to fastapi documentation we can define it like below:
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# according to the fastapi documentation, if we want sqlalchemy to talk to our database, we need to have one other thing other than
# engine as well; and it is a session defined according to the documentation like below :
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# according to fastapi documentation, we need to define class below. basically, all of our python classes that we will define later
# in "models.py" file, are going to be extended from "Base" class below:
Base = declarative_base()


# Dependency
# if you remember, in "database.py" we said that a "session" is something that is responsible for talking to our
# database. we have defined below function as a dependency, so whenever one of our API endpoints gets a request(HTTP request),
# this function below should be called. so it is going to create and assign a session for the HTTP request so that we can send sql
# queries to our database, and it will close the session whenever the request is done. this process of creating a new session for
# each HTTP request and closing it whenever it is done, will be repeated for each HTTP request when it hits one of our API
# endpoints. in summary, this function returns us a session when a request hits our endpoints. we have to pass this function
# as an argument to all of our API endpoints where we wanna perform some sort of database operation. because when a request hits an
# endpoint, the corresponding path operation function has to create a session and close it whenever the request is done. and this
# can be done only by passing below function as an argument to our API endpoints.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
