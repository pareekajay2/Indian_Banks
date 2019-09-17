import jwt
# import json
import time
import pandas as pd


def create_access_token(token):
    old = jwt.decode(token, 'secret', 'HS256')
    csv_data = pd.read_csv("tokens.csv")
    file = {str(csv_data['primary'].iloc[0]): int(csv_data['value'].iloc[0])}
    # with open('tokens.json', 'r') as infile:
    #     file = json.load(infile)
    if old['exp'] == file['exp']:
        new_exp_time = int(time.time() + 5*24*3600)
        new_token = {"exp": new_exp_time}
        data = pd.DataFrame([{'primary': 'exp', 'value': new_exp_time}])
        data.to_csv('tokens.csv', index=False)
        # with open('tokens.json', 'w') as outfile:
        #     json.dump(new_token, outfile)
        encoded_jwt = jwt.encode(new_token, 'secret', 'HS256')
        return encoded_jwt


print(str(jwt.encode({"exp": 1569082769}, 'secret', 'HS256')))

