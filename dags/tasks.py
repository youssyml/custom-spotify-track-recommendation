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


@task
def get_tracks_genres():
    import requests
    from utils import get_token_credentials
    import logging

    postgres = PostgresHook(postgres_conn_id="spotify_pg_conn")
    query = "SELECT id FROM tracks"
    track_ids = postgres.get_pandas_df(sql=query).reset_index()
    access_token = get_token_credentials()

    for i in range(0, len(track_ids), 50):
        index = i + 50 if i + 50 < len(track_ids) else len(track_ids)
        url = "https://api.spotify.com/v1/tracks"
        params = {"ids": ",".join(track_ids.id[i:index])}
        tracks_data = requests.get(
            url=url,
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
        ).json()
        logging.info(tracks_data)

        # get associated artists
        url = "https://api.spotify.com/v1/artists"
        params = {
            "ids": ",".join(
                [
                    track.get("artists")[0].get("id")
                    for track in tracks_data.get("tracks")
                ]
            )
        }
        artists_data = requests.get(
            url=url,
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
        ).json()
        for track, artist in zip(
            tracks_data.get("tracks"), artists_data.get("artists")
        ):
            # get the artists genre
            genres = artist.get("genres")

            # For each track genre, we check if it already exists
            if genres:
                for genre in genres:
                    query = "SELECT name FROM genres"
                    exist_genres = postgres.get_records(sql=query)
                    exist_genres = [t[0] for t in exist_genres]
                    # if not exists, we insert it
                    if genre not in exist_genres:
                        postgres.run(
                            sql=f"INSERT INTO genres (name) VALUES ('{genre}')"
                        )
                        # postgres.insert_rows("genres", [genre], ["name"], replace=False)

                    # get the genre id
                    query = f"SELECT id FROM genres WHERE name = '{genre}'"
                    genre_id = postgres.get_records(sql=query)[0][0]

                    # insert the tuple track x genre
                    postgres.run(
                        sql=f"INSERT INTO tracks_genres (track_id, genre_id) VALUES ('{track.get('id')}', '{genre_id}')"
                    )
