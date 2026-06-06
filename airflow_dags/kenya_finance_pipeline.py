from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'amon',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'kenya_finance_pipeline',
    default_args=default_args,
    description='Kenya Financial Inclusion - GCS to BigQuery to dbt',
    schedule='@weekly',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['kenya', 'finance', 'bigquery', 'dbt']
) as dag:

    upload_to_gcs = BashOperator(
        task_id='upload_to_gcs',
        bash_command='gsutil cp ~/Downloads/kenya_financial_inclusion.csv gs://gcp-de-learning-amon-kariuki/raw/kenya_financial_inclusion.csv'
    )

    load_to_bq = BashOperator(
        task_id='load_to_bigquery',
        bash_command='bq load --autodetect --source_format=CSV --skip_leading_rows=1 --replace kenya_finance.raw_financial_inclusion gs://gcp-de-learning-amon-kariuki/raw/kenya_financial_inclusion.csv'
    )

    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd ~/PROJECTS/dbt_projects/chicago_analysis && dbt run --select kenya'
    )

    upload_to_gcs >> load_to_bq >> run_dbt
