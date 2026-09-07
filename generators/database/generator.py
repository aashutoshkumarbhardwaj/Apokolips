import json
import random
from datetime import datetime, timedelta, timezone


SCENARIOS = [
    "normal",
    "high_load",
    "slow_queries",
    "connection_pressure",
    "storage_pressure",
    "replication_lag",
    "failure",
]


def generate_database_event(
    server_id: str,
    timestamp: datetime,
    scenario: str = "normal",
) -> dict:

    # -------------------------
    # Normal database behavior
    # -------------------------

    cpu_utilization = random.uniform(20, 70)
    memory_utilization = random.uniform(30, 75)
    disk_utilization = random.uniform(30, 70)

    active_connections = random.randint(20, 150)
    queries_per_second = random.uniform(50, 500)

    query_latency_ms = random.uniform(5, 100)

    cache_hit_ratio = random.uniform(90, 99.9)

    disk_iops = random.uniform(100, 3000)

    replication_lag_seconds = random.uniform(0, 2)

    deadlocks = random.randint(0, 1)

    error_count = random.randint(0, 2)

    # -------------------------
    # High load
    # -------------------------

    if scenario == "high_load":

        cpu_utilization = random.uniform(80, 100)
        memory_utilization = random.uniform(75, 95)

        active_connections = random.randint(150, 500)

        queries_per_second = random.uniform(500, 2000)

        query_latency_ms = random.uniform(100, 500)

        disk_iops = random.uniform(3000, 10000)

    # -------------------------
    # Slow queries
    # -------------------------

    elif scenario == "slow_queries":

        cpu_utilization = random.uniform(60, 90)
        memory_utilization = random.uniform(60, 90)

        queries_per_second = random.uniform(300, 1000)

        query_latency_ms = random.uniform(500, 5000)

        cache_hit_ratio = random.uniform(70, 90)

        deadlocks = random.randint(1, 10)

    # -------------------------
    # Connection pressure
    # -------------------------

    elif scenario == "connection_pressure":

        cpu_utilization = random.uniform(50, 85)
        memory_utilization = random.uniform(60, 90)

        active_connections = random.randint(500, 1000)

        queries_per_second = random.uniform(400, 1500)

        query_latency_ms = random.uniform(200, 1000)

    # -------------------------
    # Storage pressure
    # -------------------------

    elif scenario == "storage_pressure":

        cpu_utilization = random.uniform(40, 80)
        memory_utilization = random.uniform(50, 85)

        disk_utilization = random.uniform(90, 99.9)

        disk_iops = random.uniform(4000, 12000)

        query_latency_ms = random.uniform(100, 1000)

    # -------------------------
    # Replication lag
    # -------------------------

    elif scenario == "replication_lag":

        cpu_utilization = random.uniform(60, 90)

        queries_per_second = random.uniform(500, 1500)

        query_latency_ms = random.uniform(100, 800)

        replication_lag_seconds = random.uniform(30, 600)

        error_count = random.randint(2, 10)

    # -------------------------
    # Database failure
    # -------------------------

    elif scenario == "failure":

        cpu_utilization = random.uniform(90, 100)
        memory_utilization = random.uniform(90, 100)
        disk_utilization = random.uniform(95, 100)

        active_connections = random.randint(800, 1500)

        queries_per_second = random.uniform(1000, 2500)

        query_latency_ms = random.uniform(2000, 10000)

        cache_hit_ratio = random.uniform(50, 75)

        disk_iops = random.uniform(8000, 15000)

        replication_lag_seconds = random.uniform(300, 1200)

        deadlocks = random.randint(10, 50)

        error_count = random.randint(20, 100)

    return {
        "timestamp": timestamp.isoformat(),

        "server_id": server_id,

        "asset_type": "database",

        "cpu_utilization": round(cpu_utilization, 2),

        "memory_utilization": round(memory_utilization, 2),

        "disk_utilization": round(disk_utilization, 2),

        "active_connections": active_connections,

        "queries_per_second": round(queries_per_second, 2),

        "query_latency_ms": round(query_latency_ms, 2),

        "cache_hit_ratio": round(cache_hit_ratio, 2),

        "disk_iops": round(disk_iops, 2),

        "replication_lag_seconds": round(
            replication_lag_seconds,
            2,
        ),

        "deadlocks": deadlocks,

        "error_count": error_count,

        "scenario": scenario,

        "failure": scenario == "failure",
    }


def generate_dataset(
    num_servers: int,
    events_per_server: int,
    output_file: str,
) -> None:

    start_time = datetime.now(timezone.utc)

    total_events = 0

    with open(output_file, "w") as file:

        for server_number in range(1, num_servers + 1):

            server_id = f"db-server-{server_number:03d}"

            for event_number in range(events_per_server):

                timestamp = start_time + timedelta(
                    seconds=event_number
                )

                scenario = random.choices(
                    SCENARIOS,
                    weights=[
                        0.75,  # normal
                        0.07,  # high load
                        0.05,  # slow queries
                        0.04,  # connection pressure
                        0.04,  # storage pressure
                        0.03,  # replication lag
                        0.02,  # failure
                    ],
                )[0]

                event = generate_database_event(
                    server_id=server_id,
                    timestamp=timestamp,
                    scenario=scenario,
                )

                file.write(
                    json.dumps(event) + "\n"
                )

                total_events += 1

    print(
        f"Generated {total_events:,} database telemetry events."
    )

    print(f"Output: {output_file}")