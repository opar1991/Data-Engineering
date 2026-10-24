from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


def build_sales_summary():
    print("Bulding dairy sales summary report")
    print("Report Genrated successfully at 7.00am...")

default_args = {
    "owner": "data_team",
    "depends_on_past":False,
    "retries":1,
    "retry_delay": timedelta(minutes=1)
}

#create dag

with DAG(
    dag_id = "daily_sales_summary",
    default_args = default_args,
    description = "Gnerate Daily sales summary at 7:00am",
    start_date =datetime(2026, 10, 25),
    schedule_interval ="0 7 * * *",
    catchup=False,
    max_active_runs = 1,
    tags=["sales", "reporting"]
) as dag:
    generate_report = PythonOperator(
        task_id="Daily_sales_report",
        python_callable=build_sales_summary

    )
