from pyspark.sql.types import (
    BooleanType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)


GPU_SCHEMA = StructType([
    StructField("timestamp", TimestampType(), False),
    StructField("server_id", StringType(), False),
    StructField("gpu_id", StringType(), False),
    StructField("asset_type", StringType(), False),
    StructField("gpu_utilization", DoubleType(), False),
    StructField("gpu_memory_utilization", DoubleType(), False),
    StructField("temperature_celsius", DoubleType(), False),
    StructField("power_usage_watts", DoubleType(), False),
    StructField("ecc_errors", IntegerType(), False),
    StructField("memory_errors", IntegerType(), False),
    StructField("scenario", StringType(), False),
    StructField("failure", BooleanType(), False),
])


DATABASE_SCHEMA = StructType([
    StructField("timestamp", TimestampType(), False),
    StructField("server_id", StringType(), False),
    StructField("asset_type", StringType(), False),
    StructField("cpu_utilization", DoubleType(), False),
    StructField("memory_utilization", DoubleType(), False),
    StructField("disk_utilization", DoubleType(), False),
    StructField("active_connections", IntegerType(), False),
    StructField("queries_per_second", DoubleType(), False),
    StructField("query_latency_ms", DoubleType(), False),
    StructField("cache_hit_ratio", DoubleType(), False),
    StructField("disk_iops", DoubleType(), False),
    StructField("replication_lag_seconds", DoubleType(), False),
    StructField("deadlocks", IntegerType(), False),
    StructField("error_count", IntegerType(), False),
    StructField("scenario", StringType(), False),
    StructField("failure", BooleanType(), False),
])


KUBERNETES_SCHEMA = StructType([
    StructField("timestamp", TimestampType(), False),
    StructField("node_id", StringType(), False),
    StructField("pod_id", StringType(), False),
    StructField("asset_type", StringType(), False),
    StructField("node_cpu_utilization", DoubleType(), False),
    StructField("node_memory_utilization", DoubleType(), False),
    StructField("pod_cpu_utilization", DoubleType(), False),
    StructField("pod_memory_utilization", DoubleType(), False),
    StructField("pod_restarts", IntegerType(), False),
    StructField("disk_utilization", DoubleType(), False),
    StructField("network_receive_mbps", DoubleType(), False),
    StructField("network_transmit_mbps", DoubleType(), False),
    StructField("error_count", IntegerType(), False),
    StructField("pod_status", StringType(), False),
    StructField("node_status", StringType(), False),
    StructField("scenario", StringType(), False),
    StructField("failure", BooleanType(), False),
])