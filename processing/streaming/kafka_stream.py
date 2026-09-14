from pyspark.sql import DataFrame
from pyspark.sql.functions import col, from_json

from processing.streaming.spark_session import create_spark_session
from processing.streaming.schemas.telemetry_schema import (
    GPU_SCHEMA,
    DATABASE_SCHEMA,
    KUBERNETES_SCHEMA,
)
from data_quality.validators import add_quality_flags


KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

KAFKA_TOPICS = ",".join(
    [
        "gpu-telemetry",
        "database-telemetry",
        "kubernetes-telemetry",
    ]
)


def create_kafka_stream(spark) -> DataFrame:
    return (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
        .option("subscribe", KAFKA_TOPICS)
        .option("startingOffsets", "earliest")
        .load()
    )


def main():
    spark = create_spark_session()

    stream_df = create_kafka_stream(spark)

    parsed_df = (
        stream_df
        .select(
            col("topic"),
            col("partition"),
            col("offset"),
            col("timestamp").alias("kafka_timestamp"),
            col("value").cast("string").alias("json_value"),
        )
    )

    gpu_df = (
        parsed_df
        .filter(col("topic") == "gpu-telemetry")
        .withColumn(
            "telemetry",
            from_json(col("json_value"), GPU_SCHEMA),
        )
        .select(
            "topic",
            "partition",
            "offset",
            "kafka_timestamp",
            "telemetry.*",
        )
    )

    gpu_flagged = add_quality_flags(gpu_df)

    query = (
        gpu_flagged
        .writeStream
        .format("console")
        .outputMode("append")
        .option("truncate", "false")
        .option("numRows", 5)
        .option(
            "checkpointLocation",
            "data/processed/checkpoints/gpu_stream",
        )
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()