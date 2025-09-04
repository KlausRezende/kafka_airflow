import yaml
from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from libs.log import log_callback_success, log_callback_fail
from streaming_functions import continuous_producer_consumer

# Load parameters from YAML
with open('/opt/airflow/dags/parameters_continuous_streaming.yaml', 'r') as f:
    params = yaml.safe_load(f)

default_args = {
    'owner': params['config']['owner'],
    'retries': params['config']['retries'],
    'retry_delay': timedelta(minutes=params['config']['retry_delay_minutes'])
}

with DAG(
    dag_id=params['config']['dag_name'],
    start_date=datetime(2023, 12, 31),
    schedule_interval=params['config']['schedule_interval'],
    catchup=False,
    default_args=default_args,
    on_success_callback=log_callback_success,
    on_failure_callback=log_callback_fail
) as dag:

    start = EmptyOperator(task_id='start_continuous')
    
    streaming_task = PythonOperator(
        task_id='continuous_producer_consumer',
        python_callable=continuous_producer_consumer,
        execution_timeout=timedelta(minutes=params['config']['execution_timeout_minutes'])
    )
    
    end = EmptyOperator(task_id='end_continuous')
    
    start >> streaming_task >> end
