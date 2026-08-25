"""Module DAG"""
import os
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
from scripts.extract_load_logic import load_to_exploded_tbl, extract_from_json
from scripts.analytics_tbl import t_store_sales_summary
from airflow import DAG
from airflow.sdk import task, dag

load_dotenv()

pg_user = os.environ.get("POSTGRES_USER")
pg_db = os.environ.get("POSTGRES_DB")
pg_pwd = os.environ.get("POSTGRES_PASSWORD")
pg_host = os.environ.get("POSTGRES_HOST")

conn_db = psycopg2.connect(
    host=pg_host,
    database=pg_db,
    user=pg_user,
    password=pg_pwd
)

default_args = {
    "owner": "Germain",
    "retries": 0,
    "start_date": datetime(2026, 8, 23),
    "is_paused_upon_creation": True
}

@dag(
    dag_id="etl_sport_retail_store",
    default_args=default_args,
    description="etl retail store",
    tags=["etl", "retail store"],
    schedule="@daily",
    catchup=False
)
def etl_sport_retail_store_dag() -> None:
    """DAG"""

    @task()
    def execute_extract_load_task() -> None:
        return load_to_exploded_tbl(
            conn_db,
            extract_from_json("/opt/airflow/dags/data/pos_sales_data_30k.json")
        )

    @task
    def execute_store_sales_summary() -> None:
        return t_store_sales_summary(conn_db)

    extract_load_task = execute_extract_load_task()
    create_store_sales_summary_task = execute_store_sales_summary()

    extract_load_task >> create_store_sales_summary_task

etl_sport_retail_store_dag()
