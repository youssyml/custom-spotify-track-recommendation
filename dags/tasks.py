from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook


@task
def get_tracks_features():
    """
    Fetches all relevant track audio features
    """
    import pandas as pd
    import requests
    from utils import get_token_credentials

    access_token = get_token_credentials()

    tracks = pd.read_csv("dags/data/saved.csv")
    tracks_data = []
    url = "https://api.spotify.com/v1/audio-features"
    COLUMN_NAMES = [
        "id",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
        "time_signature",
    ]
    for i in range(0, len(tracks.id), 100):
        index = i + 100 if i + 100 < len(tracks.id) else len(tracks.id)
        params = {"ids": ",".join(tracks.id[i:index])}
        data = requests.get(
            url=url,
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
        ).json()
        tracks_data += [
            (tuple(track.get(c) for c in COLUMN_NAMES))
            for track in data.get("audio_features")
        ]

    postgres = PostgresHook(postgres_conn_id="spotify_pg_conn")
    postgres.insert_rows(
        "tracks", tracks_data, COLUMN_NAMES, replace=True, replace_index="id"
    )
