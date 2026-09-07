import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
SCHEMA_DIR = BASE_DIR / "schemas" / "telemetry"

DATA_FILES = {
    "gpu": DATA_DIR / "gpu_telemetry.jsonl",
    "database": DATA_DIR / "database_telemetry.jsonl",
    "kubernetes": DATA_DIR / "kubernetes_telemetry.jsonl",
}


def load_schema(dataset: str) -> dict:
    """Load JSON schema for a dataset."""
    schema_path = SCHEMA_DIR / f"{dataset}.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_dataset(dataset: str) -> bool:
    """Validate a registered dataset against its schema."""
    if dataset not in DATA_FILES:
        print(f"Unknown dataset: {dataset}")
        print(f"Available datasets: {', '.join(DATA_FILES.keys())}")
        return False

    data_path = DATA_FILES[dataset]
    if not data_path.exists():
        print(f"Data file not found: {data_path}")
        return False

    schema = load_schema(dataset)
    validator = Draft202012Validator(schema)

    valid_records = 0
    invalid_records = 0

    with open(data_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            record = json.loads(line)
            errors = list(validator.iter_errors(record))

            if errors:
                invalid_records += 1
                if invalid_records <= 10:
                    print(f"\nInvalid record at line {line_number}:")
                    for error in errors:
                        print(f"  - {error.message}")
            else:
                valid_records += 1

    total_records = valid_records + invalid_records
    validity_rate = (valid_records / total_records * 100) if total_records > 0 else 0.0

    print("=" * 50)
    print(f"Dataset: {dataset}")
    print("=" * 50)
    print(f"Total records:   {total_records:,}")
    print(f"Valid records:   {valid_records:,}")
    print(f"Invalid records: {invalid_records:,}")
    print(f"Validity rate:   {validity_rate:.2f}%")
    print("=" * 50)

    return invalid_records == 0


def validate_custom_file(file_path: Path) -> bool:
    """Validate a custom JSON or JSONL file."""
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return False

    # Try to infer dataset name from content or filename
    dataset = None
    try:
        if file_path.suffix == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                sample = data[0] if isinstance(data, list) and data else data
                if isinstance(sample, dict):
                    dataset = sample.get("asset_type")
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line:
                    dataset = json.loads(first_line).get("asset_type")
    except Exception:
        pass

    if not dataset or dataset not in DATA_FILES:
        for name in DATA_FILES:
            if name in file_path.name.lower():
                dataset = name
                break

    if not dataset:
        print(f"Could not infer dataset schema for: {file_path.name}")
        return False

    schema = load_schema(dataset)
    validator = Draft202012Validator(schema)

    valid_records = 0
    invalid_records = 0

    if file_path.suffix == ".json":
        with open(file_path, "r", encoding="utf-8") as file:
            content = json.load(file)
            records = content if isinstance(content, list) else [content]
            for idx, record in enumerate(records, start=1):
                errors = list(validator.iter_errors(record))
                if errors:
                    invalid_records += 1
                    label = f"record {idx}" if isinstance(content, list) else "record"
                    print(f"\nInvalid {label} in {file_path.name}:")
                    for error in errors:
                        print(f"  - {error.message}")
                else:
                    valid_records += 1
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                errors = list(validator.iter_errors(record))
                if errors:
                    invalid_records += 1
                    print(f"\nInvalid record at line {line_number}:")
                    for error in errors:
                        print(f"  - {error.message}")
                else:
                    valid_records += 1

    total_records = valid_records + invalid_records
    validity_rate = (valid_records / total_records * 100) if total_records > 0 else 0.0

    print("=" * 50)
    print(f"Custom File: {file_path.name} (Schema: {dataset})")
    print("=" * 50)
    print(f"Total records:   {total_records:,}")
    print(f"Valid records:   {valid_records:,}")
    print(f"Invalid records: {invalid_records:,}")
    print(f"Validity rate:   {validity_rate:.2f}%")
    print("=" * 50)

    return invalid_records == 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Usage: python -m schemas.validate [dataset|file_path]")
        print(f"Available datasets: {', '.join(DATA_FILES.keys())}, all")
        return 0

    target = sys.argv[1].lower() if len(sys.argv) > 1 else "all"

    if target == "all":
        success = True
        for name in DATA_FILES:
            if not validate_dataset(name):
                success = False
        return 0 if success else 1

    if target in DATA_FILES:
        return 0 if validate_dataset(target) else 1

    custom_path = Path(sys.argv[1])
    if custom_path.exists():
        return 0 if validate_custom_file(custom_path) else 1

    print(f"Error: Unknown dataset or file not found: '{sys.argv[1]}'")
    print(f"Available datasets: {', '.join(DATA_FILES.keys())}, all")
    return 1


if __name__ == "__main__":
    sys.exit(main())