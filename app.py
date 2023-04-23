from flask import Flask, jsonify,  request
# from RSA_utils.RSA_package import rsa_utils
import os
import json


import requests
app = Flask(__name__)

import os
from dotenv import load_dotenv

load_dotenv()

def send_message(url, content):
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        'messaging': content,
    }
    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(payload),
    )
    if response.status_code != 200:
        raise ValueError('Failed to send message')
    return response.json()

@app.route("/", methods=['GET', 'POST'])
def listen():
    print(request.headers)
    
    if request.method == 'POST':
        host = request.headers.get('Referer')
        
        url = f'http://{host}/'
        print("url: ",url)
        payload = request.json
        print("Request content ", payload)
        # send_message(url, 'Message receive')
        return jsonify({"message": "Hello, world!"})

    else:
        return 'Unsupported request method.'

def main():
    app.run(port=8000)


if __name__ == "__main__":
    main()