import json

from kafka import KafkaConsumer


KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

TOPICS = [
    "gpu-telemetry",
    "database-telemetry",
    "kubernetes-telemetry",
]


def create_consumer():
    return KafkaConsumer(
        *TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="dataforge-consumer",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )


def main():
    consumer = create_consumer()

    print("DataForge Kafka consumer started.")
    print(f"Listening to topics: {TOPICS}")

    try:
        for message in consumer:
            event = message.value

            print(
                f"topic={message.topic} "
                f"partition={message.partition} "
                f"offset={message.offset} "
                f"asset_type={event.get('asset_type')}"
            )

    except KeyboardInterrupt:
        print("\nStopping consumer...")

    finally:
        consumer.close()


if __name__ == "__main__":
    main()