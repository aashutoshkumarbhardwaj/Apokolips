from generators.kubernetes.config import (
    NUM_NODES,
    PODS_PER_NODE,
    EVENTS_PER_POD,
    OUTPUT_FILE,
)

from generators.kubernetes.generator import generate_dataset


if __name__ == "__main__":

    generate_dataset(
        num_nodes=NUM_NODES,
        pods_per_node=PODS_PER_NODE,
        events_per_pod=EVENTS_PER_POD,
        output_file=OUTPUT_FILE,
    )