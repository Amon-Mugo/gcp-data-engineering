from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'amon',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'africa_data_pipeline',
    default_args=default_args,
    description='GCS to BigQuery to dbt pipeline',
    schedule='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['bigquery', 'africa', 'gcs', 'dbt']
) as dag:

    check_gcs = BashOperator(
        task_id='check_gcs_files',
        bash_command='gsutil ls gs://gcp-de-learning-amon-kariuki/raw/'
    )

    load_to_bq = BashOperator(
        task_id='load_gcs_to_bq',
        bash_command='bq load --autodetect --source_format=CSV africa_data.africa_pipeline gs://gcp-de-learning-amon-kariuki/raw/Data_Africa.csv'
    )

    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd ~/PROJECTS/dbt_projects/chicago_analysis && dbt run'
    )

    check_gcs >> load_to_bq >> run_dbt
