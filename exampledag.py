from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "data-eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": None,  # would point to a Slack alert function
}

with DAG(
    dag_id="daily_sales_pipeline",
    default_args=default_args,
    schedule_interval="0 3 * * *",  # 3am daily
    start_date=days_ago(1),
    catchup=False,
    tags=["sales", "production"],
) as dag:

    # 1. Extract: pull raw events from Kafka topic, land as Parquet in S3
    extract_raw = BashOperator(
        task_id="extract_kafka_to_s3",
        bash_command="python /opt/scripts/kafka_consumer_to_s3.py --topic sales_events --date {{ ds }}",
    )

    # 2. Transform: run Spark job to clean/dedupe/aggregate raw events
    spark_transform = BashOperator(
        task_id="spark_transform",
        bash_command=(
            "spark-submit --master yarn "
            "/opt/spark_jobs/transform_sales.py --run-date {{ ds }}"
        ),
    )

    # 3. Load: push transformed Parquet from S3 into Redshift staging table
    load_to_redshift = S3ToRedshiftOperator(
        task_id="load_staging_redshift",
        schema="staging",
        table="sales_events",
        s3_bucket="my-data-lake",
        s3_key="transformed/sales/{{ ds }}/",
        redshift_conn_id="redshift_default",
        aws_conn_id="aws_default",
        copy_options=["FORMAT AS PARQUET"],
    )

    # 4. Model: run dbt to build the star schema (fact/dim tables) from staging
    run_dbt = BashOperator(
        task_id="run_dbt_models",
        bash_command="cd /opt/dbt/sales_project && dbt run --select tag:daily",
    )

    # 5. Test: run dbt tests (not_null, unique, referential integrity checks)
    test_dbt = BashOperator(
        task_id="run_dbt_tests",
        bash_command="cd /opt/dbt/sales_project && dbt test --select tag:daily",
    )

    # 6. Alert on failure (this would attach via on_failure_callback in practice)
    notify_failure = SlackWebhookOperator(
        task_id="notify_failure",
        slack_webhook_conn_id="slack_default",
        message="🚨 daily_sales_pipeline failed on task: {{ task_instance.task_id }}",
        trigger_rule="one_failed",
    )

    extract_raw >> spark_transform >> load_to_redshift >> run_dbt >> test_dbt
    [extract_raw, spark_transform, load_to_redshift, run_dbt, test_dbt] >> notify_failure