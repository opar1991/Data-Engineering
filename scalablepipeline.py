#detect all bank transactions above 1,000,000

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, desc
from pyspark.sql.types import StructField, StructType, StringType, FloatType

spark = SparkSession.builder\
.appName("Bank Transaction Monitoring-Fraud Detection")\
.getOrCreate()


schema = StructType([
    StructField("Transaction_id", StringType(), True),
    StructField("Account_Number", StringType(), True),
    StructField("Transaction_Amount", FloatType(), True),
    StructField("Transaction_Type", StringType(), True),
    StructField("Transaction_Date", StringType(), True),
    ])

data = [
    ("TXN001", "ACC0001", 250000.50, "Deposit", "2026-09-02"),
    ("TXN002", "ACC0002", 1750000.00, "Withdrawal", "2026-09-03"),
    ("TXN003", "ACC0003", 85000.75, "Deposit", "2026-09-04"),
    ("TXN004", "ACC0004", 3200000.00, "Transfer", "2026-09-05"),
    ("TXN005", "ACC0005", 450500.25, "Deposit", "2026-09-06"),
    ("TXN006", "ACC0001", 1250000.50, "Transfer", "2026-09-07"),
    ("TXN007", "ACC0006", 75000.00, "Withdrawal", "2026-09-08"),
    ("TXN008", "ACC0007", 4800000.75, "Deposit", "2026-09-09"),
    ("TXN009", "ACC0003", 625000.00, "Transfer", "2026-09-10"),
    ("TXN010", "ACC0008", 2100000.25, "Withdrawal", "2026-09-11"),
]

df = spark.createDataFrame(data, schema=schema)

df_flagged = df.withColumn(
    "is_suspicious", when(col("Transaction_Amount")>1000000, "YES").otherwise("No")
)

df_flagged.show(truncate=False)
df_flagged.filter(col("is_suspicious")=="YES")\
    .write.mode("overwrite").parquet("suspicious_transaction.parquet")


#an ecommerce wants to track and anlyze user clickstream data to understand customer behavior
#we have click events containing, User_Id, Session_Id, Action(click, view, purchase), Page_Visited, DeviceType,Country and Timestamp

spark = SparkSession.builder\
.appName("Ecommerce Clickstream Analytics")\
.getOrCreate()


# E-commerce Clickstream Analytics

schema1 = StructType([
    StructField("User_Id", StringType(), True),
    StructField("Session_Id", StringType(), True),
    StructField("Action", StringType(), True),
    StructField("Page_Visited", StringType(), True),
    StructField("DeviceType", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("Timestamp", StringType(), True),
])

data1 = [
    ("U001", "S001", "view", "Home", "Mobile", "Kenya", "2026-10-15 09:00:00"),
    ("U001", "S001", "click", "Shoes", "Mobile", "Kenya", "2026-10-15 09:01:00"),
    ("U001", "S001", "purchase", "Checkout", "Mobile", "Kenya", "2026-10-15 09:05:00"),
    ("U002", "S002", "view", "Home", "Desktop", "Uganda", "2026-10-15 09:02:00"),
    ("U002", "S002", "click", "Electronics", "Desktop", "Uganda", "2026-10-15 09:03:00"),
    ("U003", "S003", "view", "Home", "Mobile", "Kenya", "2026-10-15 09:04:00"),
    ("U003", "S003", "click", "Shoes", "Mobile", "Kenya", "2026-10-15 09:06:00"),
    ("U004", "S004", "purchase", "Checkout", "Tablet", "Tanzania", "2026-10-15 09:07:00"),
    ("U002", "S005", "view", "Fashion", "Desktop", "Uganda", "2026-10-15 09:10:00"),
    ("U005", "S006", "click", "Electronics", "Mobile", "Rwanda", "2026-10-15 09:12:00"),
]

# Create DataFrame
df_inline = spark.createDataFrame(data1, schema=schema1)

# Classify customer activity
df_inlined_cleaned = df_inline.withColumn(
    "Activity",
    when(col("Action") == "purchase", "conversion")
    .otherwise("Browsing")
)

# Remove rows missing essential fields
df_inlined_cleaned = df_inlined_cleaned.dropna(
    subset=["User_Id", "Session_Id", "Action"]
)

# Find the top 3 pages
top_pages = df_inlined_cleaned.groupBy("Page_Visited") \
    .agg(count("*").alias("visit_count")) \
    .orderBy(desc("visit_count")) \
    .limit(3)

# Analyze device usage
device_usage = df_inlined_cleaned.groupBy("DeviceType") \
    .agg(count("*").alias("usage_count")) \
    .orderBy(desc("usage_count"))

# Display results BEFORE writing
print("CLEANED CLICKSTREAM DATA")
df_inlined_cleaned.show(truncate=False)

print("TOP 3 PAGES")
top_pages.show()

print("DEVICE USAGE")
device_usage.show()

# Save results
df_inlined_cleaned.write.mode("overwrite").parquet("customer_activity/")
top_pages.write.mode("overwrite").parquet("toppages/")
device_usage.write.mode("overwrite").parquet("most_used_devices/")

print("E-commerce analytics completed successfully!")

# Stop Spark only after both projects finish
spark.stop()
