from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def add_quality_flags(df: DataFrame) -> DataFrame:
    """Add a `quality_valid` boolean flag to a telemetry DataFrame.

    Checks core required fields across telemetry types:
    - timestamp is not null
    - identifier (server_id or node_id) is not null
    - asset_type is not null
    - scenario is not null
    - failure is not null
    """
    cols = set(df.columns)

    condition = (
        col("timestamp").isNotNull()
        & col("asset_type").isNotNull()
        & col("scenario").isNotNull()
        & col("failure").isNotNull()
    )

    if "server_id" in cols:
        condition = condition & col("server_id").isNotNull()
    elif "node_id" in cols:
        condition = condition & col("node_id").isNotNull()

    return df.withColumn("quality_valid", condition)