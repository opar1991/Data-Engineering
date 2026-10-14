import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import requests



file_path = r"C:\Users\user\Downloads\Sample+-+Superstore.csv"

df = pd.read_csv(file_path, encoding="Latin1")

print(df.head(10))

#transform

#convert discount to %tage

df["percentage_discount"] = df["Discount"]*100

print(df["percentage_discount"].head(10))
print(df.head(10))

#calculate profit magin

df["ProfitMargin"] = df["Profit"]/df["Sales"]
df.columns
print(df["ProfitMargin"])

print(df.columns.tolist())

#aggregation

#how many days does it take to ship from order date to delivery date

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
df["Delivery_Days"]= (df["Ship Date"]-df["Order Date"])
print(df["Delivery_Days"])

#sales performance by region

region_summary = df.groupby(["Region","Category"]).agg(
    {
        "Order ID":"nunique",
        "Sales":"sum",
        "Profit":"sum",
        "Discount": "mean",
        "ProfitMargin":"mean"
    }
).reset_index()

region_summary.rename(columns={
    "Order Id": "Total Orders",
    "Sales":"Total Sales",
    "Profit":"Total Profit",
    "Discount":"Average Discount(%)",
    "ProfitMargin":"Average Profit Margin"
}, inplace=True)

print(region_summary)

#elt etract load and transform

#database credentials 

username = "postgres"
password = "Com/005/12"
host = "localhost"
port = "5432"
database = "superstore"

#create connection

# Create database connection engine
engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

"""try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("Connected successfully!")
        print(result.scalar())

except SQLAlchemyError as e:
    print("Database connection failed:", e)

finally:
    engine.dispose()"""

"""load=df.to_sql("sample_superstore", engine, if_exists="replace", index=False)
if load:
    print("Data Loaded Successfully")
else:
    print("Loading failed")"""

df_total_customers = pd.read_sql("""
   SELECT COUNT(*) AS Total_Orders
   FROM sample_superstore;

""", con=engine
)
print(df_total_customers)

#working with APIS

api_url="https://open.er-api.com/v6/latest/USD"

response = requests.get(api_url, timeout=30)
response.raise_for_status()
data = response.json()

# Check whether the API request was successful
if data["result"] == "success":
    rates = data["rates"]

    # Convert exchange rates into a DataFrame
    df = pd.DataFrame(
        list(rates.items()),
        columns=["Currency", "rate_per_USD"]
    )

    print("First 5 currencies:\n", df.head())
    print("\nTotal Currencies:\n", len(df))

    # Specifically show USD to Kenyan Shillings
    print("\nUSD to KES:\n", df[df["Currency"] == "KES"])

else:
    print("API request failed:", data)



