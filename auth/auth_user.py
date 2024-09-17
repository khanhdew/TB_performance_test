from config import Config as config
import requests

def get_auth_token():
    url = config.tb_url + '/api/auth/login'
    obj = {
        "username": config.tb_username,
        "password": config.tb_password
    }
    x = requests.post(url, json=obj)
    auth_token = x.json().get("token")
    return auth_token

auth_token = get_auth_token()
auth_header = {"X-Authorization": "Bearer " + auth_token}

def refresh_token():
    global auth_token, auth_header
    auth_token = get_auth_token()
    auth_header = {"X-Authorization": "Bearer " + auth_token}