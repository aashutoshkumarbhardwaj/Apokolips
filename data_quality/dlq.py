from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def split_quality_stream(df: DataFrame) -> tuple[DataFrame, DataFrame]:
    """Split a DataFrame into valid records and Dead Letter Queue (DLQ) records.

    Returns:
        tuple(valid_df, dlq_df)
    """
    valid_df = df.filter(col("quality_valid") == True)
    dlq_df = df.filter((col("quality_valid") == False) | col("quality_valid").isNull())
    return valid_df, dlq_df


def write_dlq_stream(
    dlq_df: DataFrame,
    output_path: str = "data/processed/dlq",
    checkpoint_path: str = "data/processed/checkpoints/dlq",
):
    """Write invalid records from a streaming DataFrame to DLQ storage."""
    return (
        dlq_df
        .writeStream
        .format("json")
        .outputMode("append")
        .option("path", output_path)
        .option("checkpointLocation", checkpoint_path)
        .start()
    )
