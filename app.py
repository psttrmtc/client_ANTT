from flask import Flask, jsonify,  request
# from RSA_utils.RSA_package import rsa_utils
import os
import json

from Client import MessageSender
import requests
app = Flask(__name__)

import os
from dotenv import load_dotenv

load_dotenv()
SERVER_URL = os.getenv("SERVER_URL")
PAGE_ID = os.getenv("PAGE_ID")
client = MessageSender(SERVER_URL, PAGE_ID , "user1", "123456")


@app.route("/", methods=['GET', 'POST'])
def listen():
    print(app.config['access_token'])
    if request.method == 'POST':
        content =  send_message(SERVER_URL,'Message receive')
        return jsonify(content)

    else:
        return 'Unsupported request method.'
@app.route("/customer-responses", methods=['POST'])
def customer_response():
    if request.method == 'POST':
        print(request.json)
        return "OK"

    else:
        return 'Unsupported request method.'

@app.route("/message", methods=['POST'])
def customer_response():
    if request.method == 'POST':
        print(request.json)
        client.send_message(request.json["user_id"],request.json["message"])
        return "OK"

    else:
        return 'Unsupported request method.'
@app.route("/set_webhook", methods=['POST'])
def set_webhook():
    if request.method == 'POST':
        print(request.json)
        client.set_server_url(request.json["webhook_url"])
        return "OK"
    else:
        return 'Unsupported request method.'
def main():
    access_token = get_access_token('user1', '123456')
    print("Access Token: ", access_token)
    
    app.run(port=8000, debug=True)


if __name__ == "__main__":
    main()