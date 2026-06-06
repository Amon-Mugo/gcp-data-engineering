from google.cloud import bigquery

def load_to_bq(event, context):
    bucket = event['bucket']
    filename = event['name']
    
    print(f"File detected: {filename} in bucket: {bucket}")
    
    if not filename.endswith('.csv'):
        print("Not a CSV file, skipping")
        return
    
    client = bigquery.Client()
    
    table_id = "gcp-de-learning-498109.africa_data.auto_loaded"
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    
    uri = f"gs://{bucket}/{filename}"
    
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()
    
    print(f"Loaded {filename} into {table_id}")
