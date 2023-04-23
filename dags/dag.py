from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from tasks import get_tracks_features


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

    create_tracks_table >> get_tracks_features()


process_tracks()
