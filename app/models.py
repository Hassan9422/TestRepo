# In this file, we are going to define all the logic for creating the tables and its properties as python classes. and finally
# connecting to it within fastapi.
# we connected to our database in "database.py" file already, so now we are going to create tables, its properties, etc. as python
# classes in this file.
# every class in this file represents a table in our database.
# please have a look at sqlalchemy section in fastapi documentation here https://fastapi.tiangolo.com/tutorial/sql-databases/
# it has explained in details that what should we import and how we should define our tables etc.
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

# because all of our classes are going to be extending from "Base" class in "database.py" file, we need to import it here:
from .database import Base


class Post(Base):
    # in line above, "Post" is the name of our model or class, and it is going to be known as this name within our fastapi app,
    # but what are we going to call our table within postgres when it gets created by sqlalchemy? we can specify that name in line
    # below:
    __tablename__ = "posts"

    # defining the columns of the table:
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # line below does nothing in the database whatsoever. IT DOES NOT CREATE A NEW COLUMN IN THE DATABASE! it's just going to tell sqlalchemy
    # to fetch data based on the relationship that we have between two tables here! for example, we know that there is relationship between
    # these two models according to foreign key. so when we add below property to the current Post table, it's going to fetch data related to
    # owner based on the relationship that this table has with the "User" table. in summary, line below does nothing to the database,
    # but it tells sqlalchemy to fetch some data based on the relationship between these two tables. and the relationship between these two
    # tables has been set by foreign key.
    owner = relationship('User')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
