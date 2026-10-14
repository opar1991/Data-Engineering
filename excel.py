#handing excel file in python using pandas
import pandas as pd
import openpyxl

file_path = r'C:\Users\user\Downloads\sales_report.xlsx'

df =pd.read_excel(file_path)
print(df.head(10))

print  ("\nDATASET INFORMATION\n")
print(df.info())

print("\nSummary Statistics\n")
print(df.describe())
 #filter sales by region, for example, sales in the East region
east_sales = df.loc[df['Region'] == 'East']
print(east_sales)

#total sales by region
total_sales_by_region = df.groupby('Region')['SalesAmount'].sum().reset_index()
print(total_sales_by_region)

#save fltered data back to excel

east_sales.to_excel("west_sales.xlsx", index=False)
print("Filtered Data saved Successfully..")

#pivot table of sales by regionm

pivot_table = pd.pivot_table(
    df,
    values='SalesAmount',
    index='Region',
    columns='Category',
    aggfunc='sum',
    fill_value=0
)

print(pivot_table)

