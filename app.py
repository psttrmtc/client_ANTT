from flask import Flask, jsonify,  request
# from RSA_utils.RSA_package import rsa_utils
import os
import json


import requests
app = Flask(__name__)

import os
from dotenv import load_dotenv

load_dotenv()
SERVER_URL = os.getenv("SERVER_URL")

def get_access_token(username, password):
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        'username': username,
        'password': password
    }
    response = requests.post(
        f"{SERVER_URL}/login",
        headers=headers,
        data=json.dumps(payload),
    )
    if response.status_code != 200:
        raise ValueError('Failed to send message')
    return response.json()['access_token']

access_token = get_access_token('user1', '123456')
app.config['access_token'] = access_token


def send_message(url, content):
    headers = {
        "Authorization": f"Bearer {app.config['access_token']}",
        'Content-Type': 'application/json',
    }
    payload = {
        'messaging': content,
    }
    response = requests.get(
        f"{url}/protected",
        headers=headers,
        data=json.dumps(payload),
    )
    if response.status_code != 200:
        raise ValueError('Failed to send message')
    return response.json()

@app.route("/", methods=['GET', 'POST'])
def listen():
    print(app.config['access_token'])
    if request.method == 'POST':
        content =  send_message(SERVER_URL,'Message receive')
        return jsonify(content)

    else:
        return 'Unsupported request method.'

def main():
    access_token = get_access_token('user1', '123456')
    print("Access Token: ", access_token)
    
    app.run(port=8000, debug=True)


if __name__ == "__main__":
    main()