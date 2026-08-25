import json
from pathlib import Path


def export_openapi_to_json(app, output_file: Path):
    openapi_schema = app.openapi()
    print(f"Exporting OpenAPI schema to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, ensure_ascii=False, indent=4)
        print(f"OpenAPI schema exported to {output_file} successfully.")
    