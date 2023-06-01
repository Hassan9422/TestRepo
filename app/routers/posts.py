from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, Depends, Response, APIRouter
from sqlalchemy import func

from ..database import engine, get_db
from .. import models, schemas, utils, oath2
from sqlalchemy.orm import session

router = APIRouter(prefix='/posts', tags=['Posts'])


# remember that we have added "limit", "skip", "search" variables as query parameters.
@router.get('/', response_model=List[schemas.PostVote])
# @router.get('/')
def get_posts(db: session = Depends(get_db), current_user: int = Depends(oath2.get_current_user), limit: int = 10, skip: int = 0,
              search: Optional[str] = ""):
    '''
    # we can use the cursor object that we created above for making query to the database like below:
    cursor.execute("""SELECT * FROM posts""")
    # we use 'fetchall', because we wanna grab a bunch of posts, not just one post. if we are going to get just one
    # post, we have to use 'fetchone' instead.
    # and keep in mind that you have to always fetch the response by using fetchall or fetchone, etc.
    # otherwise it's not going to return you anything
    posts = cursor.fetchall()
    '''

    # posts = db.query(models.Post).all()

    # if you wanna only see your own created posts, not other posts; you have to return below line instead of line above:
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # if you wanna limit the number of returned posts, or you wanna skip first "n" number of posts or you wanna search in posts based on the
    # "search" query parameter, you have to do this:
    # remember, we have used "contains" method inside "filter" method to search based on provided "search" keyword. also we have used "limit"
    # method to limit the results and finally "offset" method to skip the first "skip" number of results.

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # in line beow, we wanna make the sql query to perform Join and then grouping:
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                                                                       isouter=True).group_by(models.Post.id).all()

    # posts = db.query(models.Vote.post_id, func.count(models.Vote.user_id).label("votes")).group_by(models.Vote.post_id).all()
    print(type(posts))
    print(posts)
    return posts


@router.get('/{id}', response_model=schemas.PostVote)
def get_one_post(id: int, db: session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    '''
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    one_post = cursor.fetchone()

    if not one_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id={id} does not exist!")
    '''

    # filter is equivalent of using WHERE clause in SQL. remember when we are searching for just one item in our database,
    # we have to use 'first()'.  but we wanna retrieve all data from database, we use 'all()' command at the end.
    # one_post = db.query(models.Post).filter(models.Post.id == id).first()
    one_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                        isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not one_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id={id} does not exist!")

    # if you wanna return only your own created posts, you have to add condition below into your code as well. otherwise you can delete it:
    # if one_post.owner_id != current_user.id:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You don't own this post!")

    return one_post


# keep in mind that 'Post' is a pydantic model and 'post' is variable that we want to store our pydantic model in.
# we can convert the 'post' from a pydantic model to a python dictionary using dict() method

# the created user/post is going to be stored in user object which is pydantic model. in other words, all fields that we fill in when
# we create a user/post + the added fields by sqlalchemy model which are 'id' and 'created_at' fields are going to be stored in
# 'user'/'post' object as a pydantic model.
# how does sqlalchemy add 'id' and 'created_at' fields? easy! when we create a user/post, we go ahead and call User/Post class
# in models.py, so it's going to create an object of that class, and in that class we have specified the dfault value for 'id' and
# 'created_at' fields.
@router.post('/', response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    '''
    # we have to use %s to prevent the user from possible SQL injection. because if we use f string to replace the
    # post.title, etc, it's going to allow the user to perform SQL injection.

    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""", (post.title, post.content))
    # new_post = cursor.fetchone()
    # # finalizing changes we made in database by committing it to the database
    # conn.commit()
    # return new_post
    '''

    # when we create a post in this path operation, there is no way for our API to ralize that the "owner_id" field is the sme as "id" that it
    # has taken from jwt token. actually, it has taken the user who has created the post by checking the jwt token, but it just doesn't have a
    # way to understand that "owner_id" field is equal to "id" field taken from jwt token. so when we create a post here, we have to tell our
    # API that the "owner_d" field is equal to "id" field taken from token. and we should do that, because "owner_id" field is not nullable
    # , and we have to pass it when we create posT!
    created_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post


@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: session = Depends(get_db), current_user: int = Depends(
    oath2.get_current_user)):
    '''
    cursor.execute("""update posts SET title=%s, content=%s WHERE id=%s RETURNING *""", (post.title, post.content, id))
    updated_post = cursor.fetchone()
    conn.commit()
    '''

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} does not exist!")

    if current_user.id != updated_post.owner_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You do not own this post!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete('/{id}')
def delete_post(id: int, db: session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    '''
    cursor.execute("""DELETE FROM posts WHERE id=%s returning * """, (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    '''
    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()

    if deleted_post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id={id} does not exist!")

    # you can only delete your own posts, not others posts:
    if current_user.id != deleted_post.owner_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You do not own this post!")

    post_query.delete(synchronize_session=False)
    db.commit()

    # When you delete a post, the way that fastapi works is that it doesn't return you the deleted post! it just returns you a
    # status code saying that there is no content anymore with that id number!
    return Response(status_code=status.HTTP_204_NO_CONTENT)
