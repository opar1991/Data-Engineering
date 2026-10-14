import pandas as pd


#data validation

file_path = r"C:\Users\user\Downloads\sales_data_dirty.csv"

df = pd.read_csv(file_path)

print("Initial Shape", df.shape)

print(df.head(50))

#check for missing values

print("\n Missing Values\n")
print(df.isnull().sum())

#validate data types

print("\n Data Types\n")

print(df.dtypes)

df["SalesAmount"]=pd.to_numeric(df["SalesAmount"], errors="coerce")
print(df["SalesAmount"])


print("Before Conversion")

print(df["Quantity"].head(50))

print("After Conversion")

df["Quantity"]=pd.to_numeric(df["Quantity"], errors="coerce")

print(df["Quantity"].head(50))

#check for negative or invalid values
invalid_sales = df[df["SalesAmount"]<0]
print("\n Invalid Sales Amount\n", invalid_sales)

#check for duplicate orderids

duplicate_orderid = df[df.duplicated("OrderID", keep=False)]
print("\n Duplicate Orders\n", duplicate_orderid)

#validate date format

df["OrderDate"]=pd.to_datetime(df["OrderDate"], errors="coerce")
df["DeliveryDate"]=pd.to_datetime(df["DeliveryDate"], errors="coerce")

print(df[["DeliveryDate", "OrderDate"]])

#Checking Invalid Dates

invalid_dates = df[df[["OrderDate", "DeliveryDate"]].isnull().any(axis=1)]
print("\nInvalid Dates\n", invalid_dates)

#how to apply errorhandling

#how to make sure salesamount is numeric

print("\n Q1 how to make sure salesamount is numeric?\n")
print("\nSlaes Before Conversion\n", df["SalesAmount"].head(50))

df["SalesAmount"]= pd.to_numeric(df["SalesAmount"], errors="coerce")

print("\n After Conversion\n", df["SalesAmount"].head(50))

#how do we handle negative values

print("\n How do we handle negative Values\n")
df["Discount"]=pd.to_numeric(df["Discount"], errors="coerce").fillna(0)
print("\n Discount\n", df["Discount"].head(10))

#negative sales amount count

negative_sales=df[df["SalesAmount"]<0]
print(negative_sales)
#shorter way
print("\n Negative sales Amount is: \n", (df["SalesAmount"]<0).sum())
print("\n Negative Discount Values is: \n", (df["Discount"]<0).sum())
print("\n Negative Quantity Values is: \n", (df["Quantity"]<0).sum())


