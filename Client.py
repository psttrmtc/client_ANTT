from flask import Flask, jsonify, request
import os
import json
import requests
from dotenv import load_dotenv


class MessageSender:
    def __init__(self, server_url, page_id, username, password):
        self.server_url = server_url
        self.page_id = page_id
        self.access_token = self.get_access_token(username, password)

    def get_access_token(self, username, password):
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'username': username,
            'password': password
        }
        response = requests.post(
            f"{self.server_url}/login",
            headers=headers,
            data=json.dumps(payload),
        )
        if response.status_code != 200:
            raise ValueError('Failed to get access token')
        return response.json()['access_token']

    def send_message(self, user_id, message):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            'Content-Type': 'application/json',
        }
        payload = {
            'user_id': user_id,
            'page_id': self.page_id,
            "message": message,
        }
        response = requests.get(
            f"{self.server_url}/protected",
            headers=headers,
            data=json.dumps(payload),
        )
        if response.status_code != 200:
            raise ValueError('Failed to send message')
        return response.json()


if __name__ == "__main__":
    load_dotenv()
    SERVER_URL = os.getenv("SERVER_URL")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    PAGE_ID = os.getenv("PAGE_ID")
    
    sender = MessageSender(SERVER_URL, PAGE_ID , USERNAME, PASSWORD)
    print("Access Token: ", sender.access_token)
    response = sender.send_message("user1", "page1", "Hello, world!")
    print(response)
