from generators.gpu.config import (
    NUM_SERVERS,
    GPUS_PER_SERVER,
    EVENTS_PER_GPU,
    OUTPUT_FILE,
)

from generators.gpu.generator import generate_dataset


if __name__ == "__main__":
    generate_dataset(
        num_servers=NUM_SERVERS,
        gpus_per_server=GPUS_PER_SERVER,
        events_per_gpu=EVENTS_PER_GPU,
        output_file=OUTPUT_FILE,
    )