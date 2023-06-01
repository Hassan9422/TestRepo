import requests


# Login_user
jwt_token = requests.post('http://127.0.0.1:8000/login', json={'email': 'new_email5@a.b', 'password': 'new_password'}).json()
print(jwt_token)


