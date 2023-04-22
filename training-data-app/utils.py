from google.cloud import storage
import os
from .params import *


def save_playlist_data(playlist: dict) -> list:
    """
    Arguments
        A playlist dictionnary returned by the spotify playlist endpoint
    Returns
        A list containing the track id and when it was added to the playlist
    """
    tracks = []
    for item in playlist.get("items"):
        tracks.append(
            {"added_at": item.get("added_at"), "id": item.get("track").get("id")}
        )

    return tracks


def push_to_cloud():
    """
    Pushes training data to a cloud bucket
    """
    client = storage.Client()
    bucket = client.bucket(GCP_BUCKET_NAME)

    for file in os.listdir("training-data"):
        blob = bucket.blob(file)
        blob.upload_from_filename(f"training-data/{file}")


if __name__ == "__main__":
    push_to_cloud()
