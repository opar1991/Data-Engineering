
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, desc
from pyspark.sql.types import StructField, StructType, StringType, FloatType

import os

os.environ["HADOOP_HOME"] = r"C:\hadoop"

os.makedirs(r"C:\hadoop\bin", exist_ok=True)

spark = SparkSession.builder\
.appName("Bank Transaction Monitoring-Fraud Detection")\
.getOrCreate()

print("Spark version:", spark.version)
print(
    "Hadoop version:",
    spark.sparkContext._jvm.org.apache.hadoop.util.VersionInfo.getVersion()
)

from pyspark.sql import SparkSession
import os

spark = (
    SparkSession.builder
    .appName("ParquetTest")
    .master("local[*]")
    .getOrCreate()
)

df = spark.createDataFrame(
    [(1, "Nairobi"), (2, "Mombasa")],
    ["id", "city"]
)

output_path = "C:/temp/spark_parquet_test"

df.write.mode("overwrite").parquet(output_path)

print("Parquet saved successfully!")
print(os.listdir(output_path))

spark.stop()