from airflow.decorators import dag
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from tasks import get_tracks_features, get_tracks_genres


@dag(
    dag_id="process_tracks",
    schedule_interval="@daily",
    start_date=datetime(2023, 4, 22),
)
def process_tracks():
    # task to create the table if it doesn't exist
    create_tracks_table = PostgresOperator(
        task_id="create_tracks_table",
        postgres_conn_id="spotify_pg_conn",
        sql="sql/tracks_schema.sql",
    )

    create_genres_table = PostgresOperator(
        task_id="create_genres_table",
        postgres_conn_id="spotify_pg_conn",
        sql="sql/genres_schema.sql",
    )

    create_tracks_genres_table = PostgresOperator(
        task_id="create_tracks_genres_table",
        postgres_conn_id="spotify_pg_conn",
        sql="sql/tracks_genres_schema.sql",
    )
    (
        [
            create_tracks_table,
            create_genres_table,
            create_tracks_genres_table,
        ]
        >> get_tracks_features()
        >> get_tracks_genres()
    )


process_tracks()
