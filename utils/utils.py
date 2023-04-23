from google.cloud import storage
from google.oauth2 import service_account
import os
import base64
import requests
from .params import *


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

    data = {
        "redirect_uri": REDIRECT_URI,
        "grant_type": "client_credentials",
    }

    response_token = requests.post(
        url=spotify_token_url, headers=headers, data=data
    ).json()

    return response_token.get("access_token")


def get_token_authorization(code: str) -> str:
    """
    Get access token from spotify API for Authorization code flow
    This is required when user specific data needs to be read from API
    Args
        code : code
    """
    spotify_token_url = "https://accounts.spotify.com/api/token"

    client_str = CLIENT_ID + ":" + CLIENT_SECRET

    headers = {
        "Authorization": "Basic "
        + base64.b64encode(client_str.encode("ascii")).decode("utf-8"),
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response_token = requests.post(
        url=spotify_token_url, headers=headers, data=data
    ).json()

    return response_token.get("access_token")


def push_to_cloud():
    """
    Pushes training data to a cloud bucket
    """
    credentials = service_account.Credentials.from_service_account_file(
        PATH_TO_CREDENTIALS
    )
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(GCP_BUCKET_NAME)

    for file in os.listdir("training-data"):
        blob = bucket.blob(file)
        blob.upload_from_filename(f"training-data/{file}")


if __name__ == "__main__":
    push_to_cloud()
