from generators.database.config import (
    NUM_SERVERS,
    EVENTS_PER_SERVER,
    OUTPUT_FILE,
)

from generators.database.generator import generate_dataset


if __name__ == "__main__":

    generate_dataset(
        num_servers=NUM_SERVERS,
        events_per_server=EVENTS_PER_SERVER,
        output_file=OUTPUT_FILE,
    )