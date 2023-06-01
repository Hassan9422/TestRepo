import requests
import login_requests

# The HTTP request returns a Response Object with all the response data (content, encoding, status, etc).
while True:
    try:
        # env = input("Please specify the environment you would like to use:(D: Development/ P: Production")
        env = 'd'  # line above is asking the type of environment. but we have set it to development temporarily.
        if env.lower() == 'd':
            hostname = 'http://127.0.0.1:8000/'  # your local system hostname.
            break
        elif env.lower() == 'p':
            hostname = 'http://127.0.0.1:8000/'  # this is temporary. you should enter the hostname of your production environment here.
            break
        else:
            raise ValueError
    except ValueError:
        print("Please enter 'D' for Development and 'P' for Production.")

try:
    access_token = login_requests.jwt_token['token']

    # create_one_post
    # print(requests.post(f'{hostname}posts', json={'title': 'new title', 'content': 'new content'},
    #                     headers={'Authorization': f"Bearer {access_token}"}).json())

    # get_all_posts

    # remember that query parameters come after ? mark in the URL like below. also we can use as many queriesas we want, we have to just put
    # "&" to separate them. also if we wanna type space, we have to type "%20" in the URL, like below:
    # for x in requests.get(f'{hostname}posts?search=new%20title&limit=3&skip=0', headers={'Authorization': f"Bearer {access_token}"}).json():
    for x in requests.get(f'{hostname}posts', headers={'Authorization': f"Bearer {access_token}"}).json():
        print(x)

    # get_one_post
    # print(requests.get(f'{hostname}posts/10?search=new%20title&limit=5&skip=3', headers={'Authorization': f"Bearer {access_token}"}).json())

    # update_one_post
    # print(requests.put(f'{hostname}posts/15', json={'title': 'hey', 'content': 'hru'},
    #                    headers={'Authorization': f"Bearer {access_token}"}).json())

    # delete_one_post
    # print(requests.delete(f'{hostname}posts/14', headers={'Authorization': f"Bearer {access_token}"}).status_code)

    # Voting on a post
    # vote = requests.post(f'{hostname}vote', json={'post_id': 17, 'dir': 1}, headers={'Authorization': f"Bearer {access_token}"})
    # print(vote.json())
    # print(f"status_code= {vote.status_code}")

except:
    print("You have to Login First!")
