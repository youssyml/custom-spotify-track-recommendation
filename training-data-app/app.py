import csv
import requests
import base64
import pandas as pd
from flask import Flask
from flask import redirect, request
from .params import *
from .utils import save_playlist_data


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

    response_token = requests.post(
        url=spotify_token_url, headers=headers, data=data
    ).json()

    access_token = response_token.get("access_token")

    # Getting all saved tracks
    next_page_url = "https://api.spotify.com/v1/me/tracks"
    saved_tracks = []
    while next_page_url:
        tracks = requests.get(
            url=next_page_url,
            headers={"Authorization": f"Bearer {access_token}"},
            params={"limit": 50},
        ).json()
        for track in tracks.get("items"):
            saved_tracks.append(
                {"added_at": track.get("added_at"), "id": track.get("track").get("id")}
            )
        next_page_url = tracks.get("next")

    pd.DataFrame(saved_tracks).to_csv("training-data/saved.csv", index=False)

    return "<p> Fetching data and creating the files </p>"
