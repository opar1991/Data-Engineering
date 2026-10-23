import pandas as pd
import logging
import pathlib

#configure logging to write to terminal and file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s -%(message)s"
)
#file handler to save our log

file_Handler = logging.FileHandler("etl.log", mode="w")
file_Handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_Handler.setFormatter(formatter)

logging.getLogger().addHandler(file_Handler)

url = r"C:\Users\user\Downloads\superstore_bad_data.csv"

df = pd.read_csv(url)

logging.info(f"printing head")

print(df.head(10))

#determine total sales per day

Total_Daily_Sales = df.groupby("OrderDate")["Sales"].sum().reset_index()


print(f"Total sales is: {Total_Daily_Sales}")

#management wants us to dtermine profite made by region per week

df["OrderDate"]=pd.to_datetime(df["OrderDate"])
df["Week"]=df["OrderDate"].dt.isocalendar().week

profit_per_week= df.groupby(["Week","Region"])["Profit"].sum().reset_index()

print(profit_per_week)

#monthly sales per category

df["OrderDate"]=pd.to_datetime(df["OrderDate"], errors="coerce")
df["Month"]=df["OrderDate"].dt.to_period("M")
monthly_sales = df.groupby(["Month", "Category"])["Sales"].sum().reset_index()
print(monthly_sales)

#average discount rate per refion

df["Discount"]=df["Discount"].fillna(0)
average_dicount = df.groupby("Region")["Discount"].mean().reset_index()

print(average_dicount)

#top most profitable products

top_products = df.groupby("ProductName")["Profit"].sum().reset_index()
top_products = top_products.sort_values("Profit", ascending=False).head(10)
print(top_products)









