from datetime import datetime
import pytz

utc_now = datetime.now(pytz.utc)
sp_timezone = pytz.timezone('America/Sao_Paulo')
sp_now = utc_now.astimezone(sp_timezone)
formatted_sp_now = sp_now.strftime("%y-%m-%d %H:%M:%S")

def log_callback_fail(context):
    ti = context['task_instance']
    dag_run = context.get('dag_run')
    dag_id = dag_run.dag_id
    print(f"DAG {dag_id} failed at {formatted_sp_now}")

def log_callback_success(context):
    dag_run = context.get('dag_run')
    dag_id = dag_run.dag_id
    print(f"DAG {dag_id} succeeded at {formatted_sp_now}")
