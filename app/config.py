# in this file we are going to make sure that all of our env variables are provided and their format are also correct. to do this validation
# we are gonna use pydantic library to perform validation:
from pydantic import BaseSettings


# after we create this file, we can define our env variables by going to system settings and defining all of them there. but that's a lot of
# work to do and it's unnecessary. specially we know that in the future we are going to take our app to production environment and at that time
# we need to re-define all of them again! because our env variables are going to be different on our dev and prod environments. and it's waste
# of time and unnecessary to do all this work. instead of doing it like this we define all our env variables in a single file called ".env" in
# current directory. so if in the future we take our app to prod, we need to only update ".env" file! this is much more efficient. remember
# that on production you can also define your env variables on the machine itself.
class Setting(BaseSettings):
    # here we can list all of our env variables:
    database_name: str
    database_password: str
    database_username: str
    database_hostname: str
    database_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # we are telling pydantic to import env variables from ".env" file:
    class Config:
        env_file = ".env"


setting = Setting()
