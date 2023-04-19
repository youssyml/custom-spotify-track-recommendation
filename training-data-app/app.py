import csv
import requests
import base64
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

    # getting user likes and dislikes playlists
    likes_tracks = requests.get(
        url=f"https://api.spotify.com/v1/playlists/{LIKES_PLAYLIST_ID}/tracks",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    dislikes_tracks = requests.get(
        url=f"https://api.spotify.com/v1/playlists/{DISLIKES_PLAYLIST_ID}/tracks",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    # Writing data in .csv files
    for t in [
        ("likes", save_playlist_data(likes_tracks)),
        ("dislikes", save_playlist_data(dislikes_tracks)),
    ]:
        with open(f"training-data/{t[0]}.csv", mode="w", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=t[1][0].keys())
            writer.writeheader()
            writer.writerows(t[1])

    return "<p> Fetching data and creating the files </p>"
