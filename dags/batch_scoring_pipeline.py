from datetime import datetime
import os

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_ROOT = os.environ.get("PROJECT_ROOT", "/opt/airflow/project")

with DAG(
    dag_id="customer_batch_scoring_pipeline",
    start_date=datetime(2026, 6, 7),
    schedule="@daily",
    catchup=False,
    tags=["mlops", "batch-scoring"],
) as dag:
    bootstrap_model = BashOperator(
        task_id="bootstrap_approved_model",
        bash_command=f"cd {PROJECT_ROOT} && python scripts/bootstrap_approved_model.py",
    )

    run_batch_pipeline = BashOperator(
        task_id="run_batch_pipeline",
        bash_command=f"cd {PROJECT_ROOT} && python scripts/run_batch_pipeline.py",
    )

    bootstrap_model >> run_batch_pipeline

