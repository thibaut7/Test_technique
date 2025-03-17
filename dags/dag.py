from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import json

# Load parameters from JSON file
with open('/opt/airflow/config/params.json') as f:
    params = json.load(f)

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 17),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
with DAG(
    'ssh_postgres_test',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False  # Ensure it doesn't backfill old runs
) as dag:

    # Define the SSH and PostgreSQL command
    command = """
        sshpass -p '{{ params.passphrase }}' ssh -o StrictHostKeyChecking=no -i {{ params.ssh_key }} -p {{ params.port }} {{ params.user }}@{{ params.host }} \
        "PGPASSWORD={{ params.db_password }} psql -U postgres -d {{ params.dbname }} -c 'CREATE TABLE IF NOT EXISTS test (id INT); INSERT INTO test VALUES (1);'"
    """

    # Define the BashOperator task
    test_task = BashOperator(
        task_id='test_ssh_postgres',
        bash_command=command,
        params=params,  # Pass parameters for Jinja2 rendering
        dag=dag
    )