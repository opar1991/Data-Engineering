import pandas as pd
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

"""

#remove duplcates
print(df.head())

df = df.drop_duplicates(subset=["OrderID"], keep="first")

#print unique rows after removing duplicates

print("Remaining rows after removing duplicates", len(df))

#missing discount/replace with 0

df["Discount"]=df["Discount"].fillna(0)

print(df["Discount"].isnull().sum())

#remove invalid sales record

df = df[df["Sales"]>=0]
print("Remaining rows", len(df))
#standadize region column

df["Region"]=df["Region"].str.strip().str.upper()
df["Region"]=df["Region"].replace({"N/A": "UNKNOWN", "":"UNKNOWN"})
print(df["Region"].unique())

#filter extreeme profit outlier

df=df[df["Profit"].between(-1000, 10000)]
print("Remaining rows after filtering outliers", len(df))"""

#write a python etl that
#configures logging  to display messages in jupiter and save the to etl_logging.log
#Extract data and logs the number of rows
#remove duplicate rows based on orderid and logs the number of reamining rows
#remove rows where sales are negative and logs remianing rows
#saves final data and logs comletions message

#first rest logging so that we dont get error

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

#configure logging to write to terminal and file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s -%(message)s"
)
#file handler to save our log

file_Handler = logging.FileHandler("etl_superstore.log", mode="w")
file_Handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_Handler.setFormatter(formatter)

logging.getLogger().addHandler(file_Handler)

#set our etl pipelenien

url = r"C:\Users\user\Downloads\superstore_bad_data.csv"

df = pd.read_csv(url)

logging.info(f"extracted {len(df)} rows")

df = df.drop_duplicates(subset=["OrderID"])

logging.info(f"Dublicate Entries removed only  {len(df)} rows remaining" )

df = df[df["Sales"]>=0]

logging.info(f"Invalid sales removed current rows are {len(df)} rows" )

df.to_csv("superstore_cleaned.csv", index=False)

logging.info("ETL Pipeline Comlplited Successfully")

#retail company wants to cleans sales data before loading to a datat warehouse, The etl pipline must log every step

logging.info("Pipeline starting another session...")
logging.info("Session started..")

try:
    df2 = pd.read_csv(url)
    logging.info(f"extracted {len(df2)} rows")

    #file any discount missing with 0

    df2["Discount"]=df2["Discount"].fillna(0)

    logging.info(f"Missing Discounts replaced with 0 {len(df2)} rows remaining")

    logging.info(f"Droping Duplicates orders")

    df2=df2.drop_duplicates(subset=["OrderID"])

    logging.info(f"Duplicate orders dropped only {len(df2)} remaining")

    logging.info(f"filtering out negative sales...")

    df2=df2[df2["Sales"]>=0]

    logging.info(f"Ngeative sales dropped...")

    logging.info(f"Saving final Data...")

    df2.to_csv("Cleaned_Sales_Data.csv", index=False)

    logging.info(f"{len(df2)} rows saved successfully")

    logging.info(f"Pipeline completed successfully")

except Exception as e:
    logging.error(f"Pipeline Failed...: {e}")


#using pyspark to bult etls

logging.info("starting spark session")


spark = SparkSession.builder.appName("ETL_transactions").getOrCreate()

logging.info("Etl Pipeline started successfully")














