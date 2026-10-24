from kafka import KafkaProducer
import pandas as pd
import json
import time
import os
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

file_Handler = logging.FileHandler("kafka.log", mode="w")
file_Handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_Handler.setFormatter(formatter)

logging.getLogger().addHandler(file_Handler)


logging.info(f"initializing Kfaka Server...")

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v:json.dumps(v).encode("utf-8")
)

logging.info(f"Reading folder location or data source..")

folder_path = r"C:\Users\user\Downloads\Sales Events"

logging.info(f"Streaming each .csv in the folder")

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            message = row.to_dict()
            producer.send("sales-events", value=message)
            print("{message}, sent")
            logging.info(f"{message}, sent successfully")
            time.sleep(1)
producer.flush()
print("ALL Messages sent ")
    




