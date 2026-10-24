from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def start_workflow():
    print(f"Staring workflow...")

def process_data():
    print(f"Processing Data...")

def end_workflow():
    print(f"workflow completed successfully..")

#create default args

default_args = {
    "owner": "airflow",
    "retries":1,
    "retry_delay": timedelta(minutes=1),

}

#create dag

with DAG(
    dag_id = "dag_task",
    default_args = default_args,
    description = "Simple DAG",
    schedule_interval ="@daily",
    start_date = datetime(2026, 10, 24),
    catchup=False
) as dag:
    start_task = PythonOperator(
        task_id="start_task",
        python_callable=start_workflow

    )
    process_task = PythonOperator(
        task_id="process_task",
        python_callable=process_data

    )
    end_task = PythonOperator(
        task_id="end_task",
        python_callable=end_workflow
    )

    #outline dependancies or workflow

    start_task>>process_task>>end_task
    