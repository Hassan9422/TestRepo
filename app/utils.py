# in this file, we are going to store some utilities, including hashing logic


# we need this to perform the password hashing:
from passlib.context import CryptContext

# here we wanna specify the hashing algorithm. we use "bcrypt".
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
