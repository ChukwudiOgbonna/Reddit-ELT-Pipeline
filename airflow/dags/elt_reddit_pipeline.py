import pathlib
import configparser
import sys
from airflow import DAG
from airflow.operators import *
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.models.connection import Connection
from airflow.utils.dates import days_ago
import os
from datetime import timedelta, datetime


# Load Redshift Credentials
output_name = datetime.now().strftime("%Y%m%d")
parser = configparser.ConfigParser()
script_path = "/opt/airflow/extraction/"
parser.read(f"{script_path}/configuration.conf")
USERNAME = parser.get("aws_config", "redshift_username")
PASSWORD = parser.get("aws_config", "redshift_password")
HOST = parser.get("aws_config", "redshift_hostname")
PORT = parser.get("aws_config", "redshift_port")
DATABASE = parser.get("aws_config", "redshift_database")
BUCKET_NAME = parser.get("aws_config", "bucket_name")
FILENAME = f"{output_name}.csv"
LOGIN = parser.get("aws_config", "aws_access_key_id")
SECRET = parser.get("aws_config", "aws_secret_access_key")
REGION = parser.get("aws_config", "aws_region")

# Redshift Connection
conn = Connection(
    conn_id="REDSHIFT",
    conn_type="redshift",
    host= HOST,
    schema=DATABASE,
    login=USERNAME,
    password=PASSWORD,
    port=PORT
)

os.environ['AIRFLOW_CONN_REDSHIFT'] = conn.get_uri()


 

schedule_interval = "@daily"
start_date = days_ago(1)

default_args = {"owner": "airflow", "depends_on_past": False, "retries": 1}

with DAG(
    dag_id="elt_reddit_pipeline",
    description="Reddit ELT",
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1,
    tags=["RedditETL"],
    template_searchpath='/opt/airflow/extraction/',
) as dag:

    extract_reddit_data = BashOperator(
         task_id = "extract_reddit_data",
         bash_command=f"python /opt/airflow/extraction/extract_from_reddit.py {output_name}",
         dag=dag
    )

    upload_to_s3 = BashOperator(
        task_id = "upload_to_s3",
        bash_command=f"python /opt/airflow/extraction/upload_to_s3.py {output_name}",
        dag=dag
    )
    create_redshift_table = RedshiftSQLOperator(
        task_id='create_redshift_table',
        sql = 'redshift_create_table.sql',
        redshift_conn_id = conn.conn_id,
        dag = dag
    )
    create_stage_table = RedshiftSQLOperator(
        task_id='create_stage_table',
        sql = 'redshift_create_staging_table.sql',
        redshift_conn_id = conn.conn_id,
        dag = dag
    )


    s3_to_staging_area= RedshiftSQLOperator(
        task_id = "s3_to_staging_area",
        sql = "s3_to_staging_area.sql",
        redshift_conn_id = conn.conn_id,
        params ={"login" : LOGIN, "secret" : SECRET, "location" : f"s3://{BUCKET_NAME}/{FILENAME}"},
        dag = dag
    )
    update_redshift = RedshiftSQLOperator(
        task_id='update_redshift',
        sql = 'update_redshift.sql',
        redshift_conn_id = conn.conn_id,
        dag = dag
    )

    insert_redshift = RedshiftSQLOperator(
        task_id='insert_redshift',
        sql = 'insert_table.sql',
        redshift_conn_id = conn.conn_id,
        dag = dag
    )

    drop_table= RedshiftSQLOperator(
        task_id = "drop_table",
        sql = "drop_table.sql",
        redshift_conn_id = conn.conn_id,
        dag = dag
    )

    

 

    extract_reddit_data >> upload_to_s3 >>create_redshift_table >> create_stage_table >> s3_to_staging_area >> update_redshift >> insert_redshift>> drop_table




    

