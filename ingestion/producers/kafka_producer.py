import json
from pathlib import Path

from kafka import KafkaProducer


BASE_DIR = Path(__file__).resolve().parents[2]

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"


TOPICS = {
    "gpu": "gpu-telemetry",
    "database": "database-telemetry",
    "kubernetes": "kubernetes-telemetry",
}


DATA_FILES = {
    "gpu": BASE_DIR / "data/raw/gpu_telemetry.jsonl",
    "database": BASE_DIR / "data/raw/database_telemetry.jsonl",
    "kubernetes": BASE_DIR / "data/raw/kubernetes_telemetry.jsonl",
}


def create_producer():

    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,

        value_serializer=lambda value:
            json.dumps(value).encode("utf-8"),

        acks="all",

        retries=5,
    )


def publish_file(
    producer,
    dataset_name: str,
):

    topic = TOPICS[dataset_name]
    data_file = DATA_FILES[dataset_name]

    print(
        f"Publishing {dataset_name} "
        f"telemetry to {topic}..."
    )

    with open(data_file, "r") as file:

        for line in file:

            event = json.loads(line)

            producer.send(
                topic,
                value=event,
            )

    producer.flush()

    print(
        f"Finished publishing {dataset_name}."
    )


def main():

    producer = create_producer()

    for dataset_name in TOPICS:

        publish_file(
            producer,
            dataset_name,
        )

    producer.close()


if __name__ == "__main__":
    main()