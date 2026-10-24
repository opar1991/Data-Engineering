import pandas as pd
from datetime import datetime, timedelta
#from airflow import DAG
#from airflow.operators.python import PythonOperator
import logging


#first rest logging so that we dont get error

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

#configure logging to write to terminal and file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s -%(message)s"
)
#file handler to save our log

file_Handler = logging.FileHandler("banktrasanctions.log", mode="w")
file_Handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_Handler.setFormatter(formatter)

logging.getLogger().addHandler(file_Handler)

def extract_data():
    try:
        file_path = r"C:\Users\user\Downloads\transactions_2025.csv"
        df = pd.read_csv(file_path)
        logging.info(f"Data extracted successfully...")
        print(f"Total Extracted rows: {len(df)}")
        print("sample data preview")
        print(df.head(10))
        return df
    except FileNotFoundError:
        print("ERROR: FILE NOT FOUND, Please check the file path and try again")
    except Exception as e:
        print(f"Unexpected error: {e}")

extract_data()




    
        

