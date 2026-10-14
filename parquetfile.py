import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
import os

file_path = r"C:\Users\user\Downloads\sales_report+(1).csv"

#df = pd.read_csv(file_path)

#df.to_parquet("sales_report.parquet", engine="pyarrow", index=False)

print('Saving File to Parquest...')

print('Sales Report Saved as Parquet..')

data = pd.read_parquet("sales_report.parquet", engine="pyarrow")
print('Data from Paquet')
print(data.head(6))

#query specific columns

df_small = pd.read_parquet("sales_report.parquet", engine="pyarrow", columns=['OrderID', 'SalesAmount'])

print(df_small.head(20))

#apend new data

#create a dataset

new_data = {
    "OrderID": range(1, 101),
    "Product": np.random.choice(
        ["Laptop", "Phone", "Tablet", "Monitor"], 100
    ),
    "Category": np.random.choice(
        ["Electronics", "Accessories"], 100
    ),
    "Quantity": np.random.randint(5, 20, 100),
    "Price": np.random.randint(1000, 3001, 100),
    "Region": np.random.choice(
        ["North", "South", "East", "West"], 100
    ),
    "Sales Person": np.random.choice(
        ["Alice", "Bobby", "Charles", "Pascal"], 100
    ),
    "Date": pd.date_range("2024-01-01", periods=100, freq="D")
}

df = pd.DataFrame(new_data)

# Save as a Parquet file
print("Saving file...")

df.to_parquet(
    "sales_report2.parquet",
    engine="pyarrow",
    index=False
)

print("File saved successfully!")

print(df.head())

#read file

df_check = pd.read_parquet("sales_report2.parquet")
print(df_check.head(20))

#combine two files

df_old = pd.read_parquet("sales_report.parquet")
current_data = {
    "OrderId":range(df_old["OrderID"].max()+ 1, df_old["OrderID"].max()+11),
    "Product":np.random.choice(["Phone", "Tablet", "Laptop", "Monitor"],10),
    "Category":np.random.choice(["Electronic", "Accessories"],10),
    "Quantity":np.random.randint(1,10,10),
    "Price":np.random.randint(200, 2000, 10),
    "Region":np.random.choice(["East", "West", "South", "North"], 10),
    "Salesperson": np.random.choice(["Alice", "Bobby", "Charles", "Pascal"], 10 ),
     "Date": pd.date_range("2026-01-01", periods=10, freq="D")
}

df_current = pd.DataFrame(current_data)



df_combine = pd.concat([df_old, df_current], ignore_index=True)

df_combine["Date"] = pd.to_datetime(
    df_combine["Date"],
    errors="coerce"
)

df_combine.to_parquet("sales_report_final.parquet", engine="pyarrow", index=False)

print("Successfully Saved!...")
#check last few rows

print(df_combine.tail(10))

#compare the compression csv and parquet file

csv_size = os.path.getsize(file_path)/1024/1024
parquet_file_size = os.path.getsize(r"C:\Users\user\OneDrive\Desktop\Data engineering\sales_report.parquet")/1024/1024

if csv_size > parquet_file_size:
    print("CSV FILE SIZE IS: ", csv_size)
else:
    print("PARQUET FILE SIZE IS: ",parquet_file_size)

#partition with parquet

df_csv = pd.read_csv(file_path)

output_dir = r"C:\Users\user\Downloads\partitioned_sales_report.csv"
os.makedirs(output_dir, exist_ok=True)

df.to_parquet(output_dir, engine="pyarrow", partition_cols=["Region"], index=False)

print("Partioned dataset parquest saved successfully: ")

print("Created partitions:", os.listdir(output_dir))

#start spark session

spark = SparkSession.builder.appName("ParquetLession").getOrCreate()

df_spark = spark.read.parquet("sales_report.parquet")

df_spark.printSchema()

df_spark.groupBy("Region").sum("SalesAmount").show()

#average sales per region

spark = SparkSession.builder.appName("ParquetAgreegate").getOrCreate()

df_spark = spark.read.parquet("sales_report.parquet")

df_spark.printSchema()

df_spark.groupBy("Region").avg("SalesAmount").show()
#maximum sales per product
df_spark.groupBy("Product").max("SalesAmount").show()



















