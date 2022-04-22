import json

import requests
from requests import HTTPError

from objects import glob
from objects.glob import get_url, config_proxy


def user_authorize(code: str) -> dict[str, str]:
    result = {}
    req_header = {
        'Content-Type': "application/json",
        "Accept": "application/json",
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    data = json.dumps({
        "client_id": glob.config_oauth['client_id'],
        "client_secret": glob.config_oauth['client_secret'],
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": get_url("oauth/token")
    })
    response = requests.post("https://osu.ppy.sh/oauth/token", data=data, headers=req_header, proxies=config_proxy)
    if response.status_code == 200:
        result['token'] = response.json()['access_token']
        req_header['Authorization'] = f"Bearer {result['token']}"
        response = requests.get("https://osu.ppy.sh/api/v2/me", headers=req_header, proxies=config_proxy)
        if response.status_code == 200:
            rep_json = response.json()
            result['avatar_url'] = rep_json['avatar_url']
            result['username'] = rep_json['username']
            result['id'] = rep_json['id']
            return result
    raise HTTPError(response.json())
