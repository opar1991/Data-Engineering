import pandas as pd
import logging
import pathlib
import time


file_path = r"C:\Users\user\Downloads\transaction.csv"
file2 =r"C:\Users\user\Downloads\New_data.csv"
file3=r"C:\Users\user\Downloads\New_batch.csv"

df = pd.read_csv(file_path)

print(df.head(10))

for index, row in df.iterrows():
    print(f" Streaming Transactions Now->D:{row["TransactionID"]}, "
          f"Customer {row["CustomerID"]},"
          f"Amount: {row["Amount"]}, "
          f"Time {row["Timestamp"]}, "
          f"Status {row["Status"]}")

#transaction stream is one by one how can we track total completed, 
# pending, fradulatent, and total transactios

Total_Transactions = 0
Pending_Transactions = 0
Completed_Transactions =0
Failed_Trascations = 0
Fradulet_Transactions=0

for index, row in df.iterrows():
    Total_Transactions+=1
    if row["Status"]=="Completed":
        Completed_Transactions+=1
    elif row["Status"]== "Failed":
        Failed_Trascations+=1
    elif row["Status"]=="Pending":
        Pending_Transactions+=1
    elif row["Amount"]>=10000:
        Fradulet_Transactions+=1
    else:
        print("No row Found")
#printing streaming

print(f"\n Running Trasactions Records: {Total_Transactions}:->"
      f"ID: {row["TransactionID"]}, {row["CustomerID"]}, "
      F"Amount: {row["Amount"]}, {row["Status"]}")

#print running status
print("Total Transactions are:", Total_Transactions)
print("Fradulent Transactions",Fradulet_Transactions)
print("Failed Transactions",Failed_Trascations)
print("Pending transactions",Pending_Transactions)
print("Completed Transactions",Completed_Transactions)
time.sleep(4)
