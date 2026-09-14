import os
from pathlib import Path

# Ensure JAVA_HOME is configured for PySpark before PySpark imports
if "JAVA_HOME" not in os.environ:
    for java_path in [
        "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home",
        "/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home",
    ]:
        if Path(java_path).exists():
            os.environ["JAVA_HOME"] = java_path
            os.environ["PATH"] = f"{java_path}/bin:{os.environ.get('PATH', '')}"
            break

from pyspark.sql import SparkSession


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder
        .appName("DataForge-Streaming")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0",
        )
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark