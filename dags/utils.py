import base64
import requests
from params import *


def get_token_credentials() -> str:
    """
    Get access token from spotify API for client credentials flow
    This is used when no user specific data needs to be read
    """
    spotify_token_url = "https://accounts.spotify.com/api/token"

    client_str = CLIENT_ID + ":" + CLIENT_SECRET

    headers = {
        "Authorization": "Basic "
        + base64.b64encode(client_str.encode("ascii")).decode("utf-8"),
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}

    response_token = requests.post(
        url=spotify_token_url, headers=headers, data=data
    ).json()

    return response_token.get("access_token")
