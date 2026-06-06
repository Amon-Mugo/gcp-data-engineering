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
    description='Query Africa data from BigQuery',
    schedule='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['bigquery', 'africa']
) as dag:

    check_connection = BashOperator(
        task_id='check_bq_connection',
        bash_command='bq query --use_legacy_sql=false "SELECT COUNT(*) FROM africa_data.africa_population_gdp"'
    )

    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd ~/PROJECTS/dbt_projects/chicago_analysis && dbt run'
    )

    check_connection >> run_dbt
