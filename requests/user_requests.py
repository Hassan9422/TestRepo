import requests
from requests_jwt import JWTAuth


# create_one_user
print(requests.post('http://127.0.0.1:8000/users', json={'email': 'new_email8@a.b', 'password': 'new_password'}).json())


# get_one_user
# print(requests.get('http://127.0.0.1:8000/users/9').json())
