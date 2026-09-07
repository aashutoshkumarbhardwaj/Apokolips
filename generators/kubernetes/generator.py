import json
import random
from datetime import datetime, timedelta, timezone


SCENARIOS = [
    "normal",
    "high_cpu",
    "memory_pressure",
    "cpu_throttling",
    "disk_pressure",
    "network_saturation",
    "pod_crash",
    "node_failure",
]


def generate_kubernetes_event(
    node_id: str,
    pod_id: str,
    timestamp: datetime,
    scenario: str = "normal",
) -> dict:

    node_cpu_utilization = random.uniform(20, 70)
    node_memory_utilization = random.uniform(30, 75)

    pod_cpu_utilization = random.uniform(10, 70)
    pod_memory_utilization = random.uniform(20, 75)

    pod_restarts = 0

    disk_utilization = random.uniform(30, 70)

    network_receive_mbps = random.uniform(10, 500)
    network_transmit_mbps = random.uniform(10, 500)

    error_count = random.randint(0, 2)

    pod_status = "Running"
    node_status = "Ready"

    # -------------------------
    # High CPU
    # -------------------------

    if scenario == "high_cpu":

        node_cpu_utilization = random.uniform(85, 100)
        pod_cpu_utilization = random.uniform(85, 100)

    # -------------------------
    # Memory pressure
    # -------------------------

    elif scenario == "memory_pressure":

        node_memory_utilization = random.uniform(90, 100)
        pod_memory_utilization = random.uniform(90, 100)

    # -------------------------
    # CPU throttling
    # -------------------------

    elif scenario == "cpu_throttling":

        node_cpu_utilization = random.uniform(75, 95)
        pod_cpu_utilization = random.uniform(90, 100)

        error_count = random.randint(2, 10)

    # -------------------------
    # Disk pressure
    # -------------------------

    elif scenario == "disk_pressure":

        disk_utilization = random.uniform(90, 100)

        error_count = random.randint(1, 8)

    # -------------------------
    # Network saturation
    # -------------------------

    elif scenario == "network_saturation":

        network_receive_mbps = random.uniform(800, 2000)
        network_transmit_mbps = random.uniform(800, 2000)

        error_count = random.randint(1, 10)

    # -------------------------
    # Pod crash
    # -------------------------

    elif scenario == "pod_crash":

        pod_restarts = random.randint(3, 20)

        pod_status = "CrashLoopBackOff"

        error_count = random.randint(5, 20)

    # -------------------------
    # Node failure
    # -------------------------

    elif scenario == "node_failure":

        node_cpu_utilization = random.uniform(95, 100)
        node_memory_utilization = random.uniform(95, 100)

        disk_utilization = random.uniform(95, 100)

        pod_status = "Unknown"
        node_status = "NotReady"

        pod_restarts = random.randint(5, 30)

        error_count = random.randint(10, 50)

    return {
        "timestamp": timestamp.isoformat(),

        "node_id": node_id,
        "pod_id": pod_id,

        "asset_type": "kubernetes",

        "node_cpu_utilization": round(
            node_cpu_utilization,
            2,
        ),

        "node_memory_utilization": round(
            node_memory_utilization,
            2,
        ),

        "pod_cpu_utilization": round(
            pod_cpu_utilization,
            2,
        ),

        "pod_memory_utilization": round(
            pod_memory_utilization,
            2,
        ),

        "pod_restarts": pod_restarts,

        "disk_utilization": round(
            disk_utilization,
            2,
        ),

        "network_receive_mbps": round(
            network_receive_mbps,
            2,
        ),

        "network_transmit_mbps": round(
            network_transmit_mbps,
            2,
        ),

        "error_count": error_count,

        "pod_status": pod_status,

        "node_status": node_status,

        "scenario": scenario,

        "failure": scenario in [
            "pod_crash",
            "node_failure",
        ],
    }


def generate_dataset(
    num_nodes: int,
    pods_per_node: int,
    events_per_pod: int,
    output_file: str,
) -> None:

    start_time = datetime.now(timezone.utc)

    total_events = 0

    with open(output_file, "w") as file:

        for node_number in range(1, num_nodes + 1):

            node_id = f"k8s-node-{node_number:03d}"

            for pod_number in range(1, pods_per_node + 1):

                pod_id = (
                    f"{node_id}-pod-{pod_number:03d}"
                )

                for event_number in range(
                    events_per_pod
                ):

                    timestamp = (
                        start_time
                        + timedelta(
                            seconds=event_number
                        )
                    )

                    scenario = random.choices(
                        SCENARIOS,
                        weights=[
                            0.75,
                            0.05,
                            0.05,
                            0.04,
                            0.04,
                            0.03,
                            0.025,
                            0.015,
                        ],
                    )[0]

                    event = generate_kubernetes_event(
                        node_id=node_id,
                        pod_id=pod_id,
                        timestamp=timestamp,
                        scenario=scenario,
                    )

                    file.write(
                        json.dumps(event) + "\n"
                    )

                    total_events += 1

    print(
        f"Generated {total_events:,} "
        "Kubernetes telemetry events."
    )

    print(
        f"Output: {output_file}"
    )