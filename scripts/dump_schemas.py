import json

from synthetic_open_schema_model.v1beta1 import ALL_TYPES


def main() -> None:
    schema = ALL_TYPES.json_schema()
    print(json.dumps(schema, indent=2))


if __name__ == "__main__":
    main()
