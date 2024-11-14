import requests

from cfg.secret import (app_name, client_id, client_secret, code, email,
                         refresh_token)
from cfg.tokens_cfg import token_request_url


def refresh_tokens():
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'User-Agent': f'{app_name} ({email})',
    }
    response = requests.post(token_request_url, headers=headers, data=data)
    return response.json()

def get_tokens():
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    headers = {
        'User-Agent': f'{app_name} ({email})',
    }
    response = requests.post(token_request_url, headers=headers, data=data)
    return response.json()