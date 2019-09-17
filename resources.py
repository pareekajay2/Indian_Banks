import jwt
import json
import time


def create_access_token(token):
    old = jwt.decode(token, 'secret', 'HS256')
    with open('tokens.json', 'r') as infile:
        file = json.load(infile)
    if old['exp'] == file['exp']:
        new_token = {"exp": int(time.time() + 5*24*3600)}
        with open('tokens.json', 'w') as outfile:
            json.dump(new_token, outfile)
        encoded_jwt = jwt.encode(new_token, 'secret', 'HS256')
        return encoded_jwt


print(str(jwt.encode({"exp": 1569082769}, 'secret', 'HS256')))

