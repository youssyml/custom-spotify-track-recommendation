from flask import Flask
from flask import redirect, request
import requests
import base64
from .params import *


app = Flask(__name__)


@app.route("/")
def index():
    spotify_login_url = "https://accounts.spotify.com/authorize?"
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": "user-library-read",
        "redirect_uri": REDIRECT_URI,
    }
    redirection_url = spotify_login_url + "&".join(
        [f"{k}={v}" for k, v in params.items()]
    )
    print(redirection_url)
    return redirect(redirection_url)


@app.route("/callback/")
def callback():
    # getting the token from spotify API
    spotify_token_url = "https://accounts.spotify.com/api/token"

    client_str = CLIENT_ID + ":" + CLIENT_SECRET

    headers = {
        "Authorization": "Basic "
        + base64.b64encode(client_str.encode("ascii")).decode("utf-8"),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "code": request.args.get("code"),
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(url=spotify_token_url, headers=headers, data=data)

    return response.json()
