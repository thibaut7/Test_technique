from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import json

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('ssh_postgres_test', default_args=default_args, schedule = '@minute' ) as dag:
    command = '''
        SSH_KEY="{{ json.load(open('/opt/airflow/config/params.json'))['ssh_key'] }}"
        PASSPHRASE="{{ json.load(open('/opt/airflow/config/params.json'))['passphrase'] }}"
        HOST="{{ json.load(open('/opt/airflow/config/params.json'))['host'] }}"
        PORT="{{ json.load(open('/opt/airflow/config/params.json'))['port'] }}"
        USER="{{ json.load(open('/opt/airflow/config/params.json'))['user'] }}"
        DBNAME="{{ json.load(open('/opt/airflow/config/params.json'))['dbname'] }}"

        sshpass -p "$PASSPHRASE" ssh -o StrictHostKeyChecking=no -i $SSH_KEY -p $PORT $USER@$HOST \
            "psql -U postgres -d $DBNAME -c 'CREATE TABLE IF NOT EXISTS test (id INT); INSERT INTO test VALUES (1);'"
    '''

    test_task = BashOperator(
        task_id='test_ssh_postgres',
        bash_command=command,
        dag=dag
    )