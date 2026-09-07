import json
import random
from datetime import datetime, timedelta, timezone


SCENARIOS = [
    "normal",
    "high_utilization",
    "thermal_spike",
    "memory_pressure",
    "ecc_error",
    "failure",
]


def generate_gpu_event(
    server_id: str,
    gpu_id: str,
    timestamp: datetime,
    scenario: str = "normal",
) -> dict:

    # -------------------------
    # Normal operating behavior
    # -------------------------

    gpu_utilization = random.uniform(20, 80)
    memory_utilization = random.uniform(20, 75)
    temperature = random.uniform(40, 70)
    power_usage = random.uniform(100, 280)

    ecc_errors = random.randint(0, 1)
    memory_errors = 0

    # -------------------------
    # High GPU utilization
    # -------------------------

    if scenario == "high_utilization":
        gpu_utilization = random.uniform(85, 100)
        memory_utilization = random.uniform(70, 95)
        temperature = random.uniform(65, 82)
        power_usage = random.uniform(280, 350)

    # -------------------------
    # Thermal spike
    # -------------------------

    elif scenario == "thermal_spike":
        gpu_utilization = random.uniform(75, 100)
        memory_utilization = random.uniform(60, 90)
        temperature = random.uniform(85, 98)
        power_usage = random.uniform(280, 360)

    # -------------------------
    # Memory pressure
    # -------------------------

    elif scenario == "memory_pressure":
        gpu_utilization = random.uniform(60, 95)
        memory_utilization = random.uniform(92, 100)
        temperature = random.uniform(65, 85)
        power_usage = random.uniform(250, 340)

    # -------------------------
    # ECC error spike
    # -------------------------

    elif scenario == "ecc_error":
        gpu_utilization = random.uniform(70, 95)
        memory_utilization = random.uniform(75, 95)
        temperature = random.uniform(70, 88)
        power_usage = random.uniform(260, 350)

        ecc_errors = random.randint(5, 20)
        memory_errors = random.randint(1, 8)

    # -------------------------
    # Imminent GPU failure
    # -------------------------

    elif scenario == "failure":
        gpu_utilization = random.uniform(85, 100)
        memory_utilization = random.uniform(90, 100)
        temperature = random.uniform(90, 105)
        power_usage = random.uniform(300, 380)

        ecc_errors = random.randint(15, 50)
        memory_errors = random.randint(5, 20)

    return {
        "timestamp": timestamp.isoformat(),
        "server_id": server_id,
        "gpu_id": gpu_id,
        "asset_type": "gpu",

        "gpu_utilization": round(gpu_utilization, 2),
        "gpu_memory_utilization": round(memory_utilization, 2),
        "temperature_celsius": round(temperature, 2),
        "power_usage_watts": round(power_usage, 2),

        "ecc_errors": ecc_errors,
        "memory_errors": memory_errors,

        "scenario": scenario,

        "failure": scenario == "failure",
    }


def generate_dataset(
    num_servers: int,
    gpus_per_server: int,
    events_per_gpu: int,
    output_file: str,
) -> None:

    start_time = datetime.now(timezone.utc)

    total_events = 0

    with open(output_file, "w") as file:

        for server_number in range(1, num_servers + 1):

            server_id = f"gpu-server-{server_number:03d}"

            for gpu_number in range(gpus_per_server):

                gpu_id = f"{server_id}-gpu-{gpu_number}"

                for event_number in range(events_per_gpu):

                    timestamp = start_time + timedelta(
                        seconds=event_number
                    )

                    # Mostly normal infrastructure behavior
                    scenario = random.choices(
                        SCENARIOS,
                        weights=[
                            0.75,  # normal
                            0.08,  # high utilization
                            0.05,  # thermal spike
                            0.05,  # memory pressure
                            0.04,  # ECC error
                            0.03,  # failure
                        ],
                    )[0]

                    event = generate_gpu_event(
                        server_id=server_id,
                        gpu_id=gpu_id,
                        timestamp=timestamp,
                        scenario=scenario,
                    )

                    file.write(json.dumps(event) + "\n")

                    total_events += 1

    print(f"Generated {total_events:,} GPU telemetry events.")
    print(f"Output: {output_file}")