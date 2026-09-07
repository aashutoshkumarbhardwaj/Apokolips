import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator


BASE_DIR = Path(__file__).resolve().parent.parent

# Registry mapping target names to their respective schema and data files
TARGET_REGISTRY = {
    "gpu": {
        "schema": BASE_DIR / "schemas" / "telemetry" / "gpu.json",
        "data": BASE_DIR / "data" / "raw" / "gpu_telemetry.jsonl",
        "asset_type": "gpu",
    },
    "database": {
        "schema": BASE_DIR / "schemas" / "telemetry" / "database.json",
        "data": BASE_DIR / "data" / "raw" / "database_telemetry.jsonl",
        "asset_type": "database",
    },
    "kubernetes": {
        "schema": BASE_DIR / "schemas" / "telemetry" / "kubernetes.json",
        "data": BASE_DIR / "data" / "raw" / "kubernetes_telemetry.jsonl",
        "asset_type": "kubernetes",
    },
}


def load_schema(schema_path: Path) -> dict:
    """Load JSON schema from disk."""
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_file(data_path: Path, schema_path: Path) -> tuple[int, int]:
    """Validate a JSON or JSONL data file against a JSON schema.

    Returns:
        (valid_count, invalid_count)
    """
    schema = load_schema(schema_path)
    validator = Draft202012Validator(schema)

    valid_records = 0
    invalid_records = 0

    if data_path.suffix == ".json":
        with open(data_path, "r", encoding="utf-8") as file:
            content = json.load(file)
            records = content if isinstance(content, list) else [content]
            for idx, record in enumerate(records, start=1):
                errors = list(validator.iter_errors(record))
                if errors:
                    invalid_records += 1
                    label = f"record {idx}" if isinstance(content, list) else "record"
                    print(f"\nInvalid {label} in {data_path.name}:")
                    for error in errors:
                        print(f"  - {error.message}")
                else:
                    valid_records += 1
    else:
        with open(data_path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                errors = list(validator.iter_errors(record))
                if errors:
                    invalid_records += 1
                    if invalid_records <= 10:  # Avoid flooding output
                        print(f"\nInvalid record at line {line_number}:")
                        for error in errors:
                            print(f"  - {error.message}")
                else:
                    valid_records += 1

    return valid_records, invalid_records


def run_target_validation(target_name: str) -> bool:
    """Validate a registered target by name (e.g. 'gpu', 'database')."""
    config = TARGET_REGISTRY[target_name]
    schema_path = config["schema"]
    data_path = config["data"]

    if not data_path.exists():
        print(f"[-] Data file not found for target '{target_name}': {data_path}")
        return False

    if not schema_path.exists():
        print(f"[-] Schema file not found for target '{target_name}': {schema_path}")
        return False

    print(f"\n{'=' * 50}")
    print(f"Validating Target : {target_name.upper()}")
    print(f"Schema Path       : {schema_path.relative_to(BASE_DIR)}")
    print(f"Data Path         : {data_path.relative_to(BASE_DIR)}")
    print(f"{'=' * 50}")

    valid_count, invalid_count = validate_file(data_path, schema_path)

    print(f"\nValidation complete for {data_path.name}:")
    print(f"  Valid records   : {valid_count:,}")
    print(f"  Invalid records : {invalid_count:,}")
    status = "PASSED" if invalid_count == 0 else "FAILED"
    print(f"  Status          : {status}")

    return invalid_count == 0


def run_custom_file_validation(file_path: Path) -> bool:
    """Validate an ad-hoc JSON/JSONL file by inferring its target schema."""
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return False

    # Infer target schema from record content or filename
    schema_path = None
    try:
        if file_path.suffix == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                sample = data[0] if isinstance(data, list) and data else data
                asset = sample.get("asset_type") if isinstance(sample, dict) else None
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                asset = json.loads(first_line).get("asset_type") if first_line else None

        if asset and asset in TARGET_REGISTRY:
            schema_path = TARGET_REGISTRY[asset]["schema"]
    except Exception:
        pass

    # Fallback to checking filename if asset_type inference didn't yield a schema
    if not schema_path:
        for name, config in TARGET_REGISTRY.items():
            if name in file_path.name.lower():
                schema_path = config["schema"]
                break

    if not schema_path or not schema_path.exists():
        print(f"Error: Could not determine valid schema for {file_path.name}.")
        return False

    print(f"\nValidating custom file: {file_path.name}")
    print(f"Using schema: {schema_path.relative_to(BASE_DIR)}")
    valid_count, invalid_count = validate_file(file_path, schema_path)
    print(f"\nValidation complete for {file_path.name}:")
    print(f"  Valid records   : {valid_count:,}")
    print(f"  Invalid records : {invalid_count:,}")
    return invalid_count == 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Usage: python -m schemas.validate [target|file_path]")
        print("\nRegistered targets:")
        for name in TARGET_REGISTRY:
            print(f"  - {name}")
        print("  - all (validates all available registered targets)")
        return 0

    target = sys.argv[1].lower() if len(sys.argv) > 1 else "all"

    if target == "all":
        available_targets = [
            t for t, cfg in TARGET_REGISTRY.items()
            if cfg["data"].exists() and cfg["schema"].exists()
        ]
        if not available_targets:
            print("No datasets found to validate.")
            return 1

        all_success = True
        for t in available_targets:
            success = run_target_validation(t)
            if not success:
                all_success = False

        print(f"\n{'=' * 50}")
        print(f"Summary: All available targets ({', '.join(available_targets)}) validated.")
        print(f"Overall Result: {'ALL PASSED' if all_success else 'SOME FAILED'}")
        print(f"{'=' * 50}")
        return 0 if all_success else 1

    if target in TARGET_REGISTRY:
        success = run_target_validation(target)
        return 0 if success else 1

    # Check if target is a file path
    path = Path(sys.argv[1])
    if path.exists():
        success = run_custom_file_validation(path)
        return 0 if success else 1

    print(f"Error: Unknown target or file not found: '{sys.argv[1]}'")
    print(f"Available targets: {', '.join(TARGET_REGISTRY.keys())}, all")
    return 1


if __name__ == "__main__":
    sys.exit(main())