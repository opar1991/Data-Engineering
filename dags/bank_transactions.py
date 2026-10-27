
import logging
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

# This directory must be mounted into the Airflow container.
DATA_DIR = Path("/opt/airflow/dags/Data")

INPUT_FILE = DATA_DIR / "transactions_2025.csv"
INTERMEDIATE_FILE = DATA_DIR / "successful_transactions.csv"
OUTPUT_FILE = DATA_DIR / "transactions_2026.csv"


def extract_data():
    try:
        df = pd.read_csv(INPUT_FILE)

        logging.info("Data extracted successfully")
        logging.info("Total extracted rows: %s", len(df))

        # Return a path, not the entire DataFrame.
        return str(INPUT_FILE)

    except Exception:
        logging.exception("Data extraction failed")
        raise


def transform_data(input_path):
    try:
        df = pd.read_csv(input_path)

        required_columns = {"status", "amount", "branch"}
        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(f"Missing columns: {missing}")

        cleaned_df = df[
            df["status"].astype(str).str.strip().str.lower()
            == "success"
        ].copy()

        cleaned_df["amount"] = pd.to_numeric(
            cleaned_df["amount"], errors="raise"
        )

        total_amount = cleaned_df["amount"].sum()
        branch_summary = cleaned_df.groupby("branch")["amount"].sum()

        logging.info("Transformation successful")
        logging.info("Successful transactions: %s", len(cleaned_df))
        logging.info("Successful amount: KES %,.2f", total_amount)
        logging.info("Branch summary:\n%s", branch_summary)

        cleaned_df.to_csv(INTERMEDIATE_FILE, index=False)

        return str(INTERMEDIATE_FILE)

    except Exception:
        logging.exception("Data transformation failed")
        raise


def load_data(input_path):
    try:
        cleaned_df = pd.read_csv(input_path)

        cleaned_df.to_csv(OUTPUT_FILE, index=False)

        logging.info("Data loaded successfully: %s rows", len(cleaned_df))
        logging.info("Output saved at: %s", OUTPUT_FILE)

    except Exception:
        logging.exception("Data loading failed")
        raise


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    dag_id="simple_etl",
    default_args=default_args,
    description="Bank transaction ETL pipeline",
    schedule="@daily",
    start_date=datetime(2026, 10, 27),
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform_data,
        op_args=[extract_task.output],
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load_data,
        op_args=[transform_task.output],
    )

    extract_task >> transform_task >> load_task
