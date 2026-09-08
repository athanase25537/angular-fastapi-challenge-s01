"""Generate TypeScript DTOs from the FastAPI OpenAPI document.

Usage: python DTOGenerator.py [--input openapi.json] [--output path/to/generated]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SKIPPED_SCHEMAS = {"HTTPValidationError", "ValidationError"}


def kebab_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def ref_name(reference: str) -> str:
    return reference.rsplit("/", 1)[-1]


def ts_type(schema: dict[str, Any]) -> str:
    if "$ref" in schema:
        return ref_name(schema["$ref"])
    if "enum" in schema:
        return " | ".join(json.dumps(value) for value in schema["enum"])
    if "anyOf" in schema or "oneOf" in schema:
        options = schema.get("anyOf", schema.get("oneOf", []))
        return " | ".join(dict.fromkeys(ts_type(option) for option in options)) or "unknown"
    if "allOf" in schema:
        return " & ".join(ts_type(option) for option in schema["allOf"]) or "unknown"
    schema_type = schema.get("type")
    if schema_type == "array":
        return f"Array<{ts_type(schema.get('items', {}))}>"
    if schema_type == "object":
        additional = schema.get("additionalProperties")
        return f"Record<string, {ts_type(additional)}>" if isinstance(additional, dict) else "Record<string, unknown>"
    if schema_type in {"integer", "number"}:
        return "number"
    if schema_type == "boolean":
        return "boolean"
    if schema_type == "null":
        return "null"
    if schema_type == "string":
        return "string"
    return "unknown"


def referenced_types(schema: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    if "$ref" in schema:
        refs.add(ref_name(schema["$ref"]))
    for value in schema.values():
        if isinstance(value, dict):
            refs |= referenced_types(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    refs |= referenced_types(item)
    return refs


def render_schema(name: str, schema: dict[str, Any]) -> str:
    refs = referenced_types(schema) - {name}
    imports = "\n".join(
        f"import type {{ {reference} }} from './{kebab_case(reference)}';"
        for reference in sorted(refs)
    )
    if imports:
        imports += "\n\n"
    if "enum" in schema:
        return f"{imports}export type {name} = {' | '.join(json.dumps(value) for value in schema['enum'])};\n"
    required = set(schema.get("required", []))
    lines = [
        f"  {property_name}{'' if property_name in required else '?'}: {ts_type(property_schema)};"
        for property_name, property_schema in schema.get("properties", {}).items()
    ]
    return f"{imports}export interface {name} {{\n" + "\n".join(lines) + "\n}\n"


def generate(openapi: dict[str, Any], output_dir: Path) -> None:
    schemas = openapi.get("components", {}).get("schemas", {})
    output_dir.mkdir(parents=True, exist_ok=True)
    names = [name for name in schemas if name not in SKIPPED_SCHEMAS]
    for name in names:
        (output_dir / f"{kebab_case(name)}.ts").write_text(render_schema(name, schemas[name]), encoding="utf-8")
    (output_dir / "index.ts").write_text(
        "\n".join(f"export type {{ {name} }} from './{kebab_case(name)}';" for name in names) + "\n",
        encoding="utf-8",
    )
    print(f"Generated {len(names)} TypeScript DTOs in {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate TypeScript DTOs from OpenAPI schemas")
    parser.add_argument("--input", default="openapi.json")
    parser.add_argument("--output", default="frontend/DTOGenerator/src/app/core/api/generated")
    args = parser.parse_args()
    with Path(args.input).open(encoding="utf-8") as source:
        generate(json.load(source), Path(args.output))


if __name__ == "__main__":
    main()
