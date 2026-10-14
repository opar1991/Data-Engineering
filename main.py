import pandas as pd
import matplotlib.pyplot as plt

file_path = r'C:\Users\user\Downloads\superstore_dataset\superstore_dataset.csv'

df = pd.read_csv(file_path)

#select top 10 rows of the dataset

print(df.head(10))

#print data information
print(df.info())
print(df.describe())    

#print selected columns of the dataset
#ensure to use actual column names from the dataset

print(df[['order_id', 'sales', 'profit']].head(10))

#filter rows based on a condition, for example, sales greater than 1000
high_sales = df[df['sales'] > 1000]
print(high_sales.head(10))

#grouping and aggregating data, for example, total sales by region
total_sales_by_region = df.groupby('region')['sales'].sum().reset_index()
print(total_sales_by_region)

#calculate profit by category
profit_by_category = df.groupby('category')['profit'].sum().reset_index()
print(profit_by_category)

#joinning data for example customers and orders
#merge customers and orders dataframes on customer_id

customers = df[['customer_id', 'region']].drop_duplicates()
orders = df[['order_id', 'customer_id', 'sales', 'profit']]
merged_data = pd.merge(orders, customers, on='customer_id', how='inner')

print(merged_data.head(10))

#apply transformations, on our dataset, for example, classify sales into high and low categories based on a threshold
def classify_sales(sales):
    if sales > 1000:
        return 'High'
    elif sales>500 and sales <= 1000:
        return 'Medium'
    else:
        return 'Low'


#apply the transformation to the sales column
df['sales_category'] = df['sales'].apply(classify_sales)
print(df[['order_id', 'sales', 'sales_category']].head(10))

#calculate profit margin

df['profit_margin'] = (df['profit'] / df['sales'])
print(df[['order_id', 'sales', 'profit', 'profit_margin']].head(10))

#sorting and ranking, eg top customers based on sales
top_customers = df.groupby('customer_id')['sales'].sum().reset_index().sort_values(by='sales', ascending=False)
print(top_customers.head(10))

#handling missing data or empty values, or null values
print(df.isnull().sum())

#filling missing values

df['profit']=df['profit'].fillna(0, inplace=False)   
df['region']=df['region'].fillna('Unknown', inplace=False)   
df['category']=df['category'].fillna('Unknown', inplace=False)   
df['sales']=df['sales'].fillna(0, inplace=False) 

#sales and profit by region

sales_profit_by_region = df.groupby('region')[['sales', 'profit']].sum().reset_index()
print(sales_profit_by_region)

#multiple aggregations
#for ssales and profit per regions

agg_result= df.groupby('region').agg(
    total_sales=('sales', 'sum'),
    avg_sales=('sales', 'mean'),
    total_profit=('profit', 'sum'),
    avg_profit=('profit', 'mean'),
    order_count=('order_id', 'count')
   ).reset_index()

print(agg_result)

#determine pivot table category vs region

pivot_table = pd.pivot_table(
    df, values='sales', 
    index='category', 
    columns='region', 
    aggfunc='sum',
    fill_value=0)
print(pivot_table)

#how to convert to a date format
df['order_date'] = pd.to_datetime(df['order_date'])
df['year']=df['order_date'].dt.year
df['month']=df['order_date'].dt.month

print(df[['order_id', 'order_date', 'year', 'month']].head(10))

#find the top 5 categories based on sales and plot them
"""
df_top_categories = df.groupby('category')['sales'].sum().reset_index()
df_top_categories = df_top_categories.sort_values(by='sales', ascending=False).head(5)
print(df_top_categories)
#plotting the top 5 categories based on sales
plt.figure(figsize=(10,6))
plt.bar(df_top_categories['category'], df_top_categories['sales'])
plt.xlabel('Category', fontsize=12, fontweight='bold')
plt.ylabel('Sales', fontsize=12, fontweight='bold')
plt.title('Top 5 Categories by Sales', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.show()"""

df_top_categories = (
    df.groupby('category')['sales']
    .sum()
    .reset_index()
)

df_top_categories = (
    df_top_categories
    .sort_values(by='sales', ascending=False)
    .head(5)
)

print(df_top_categories)

# Plotting the top 5 categories based on sales

colors = ['blue', 'green', 'orange', 'red', 'purple']
plt.figure(figsize=(10, 6))

plt.bar(
    df_top_categories['category'],
    df_top_categories['sales'],
    color=colors
)


plt.xlabel(
    'Category',
    fontsize=12,
    fontweight='bold'
)

plt.ylabel(
    'Sales',
    fontsize=12,
    fontweight='bold'
)

plt.title(
    'Top 5 Categories by Sales',
    fontsize=14,
    fontweight='bold'
)

plt.xticks(rotation=45)

# Add values above bars
for category, sales in zip(
    df_top_categories['category'],
    df_top_categories['sales']
):
    plt.text(
        category,
        sales,
        f'{sales:,.0f}',
        ha='center',
        va='bottom',
        fontweight='bold'
    )

plt.tight_layout()
plt.show()









