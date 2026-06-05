#!/usr/bin/env python3
"""
validate.py — completeness checker for chonk-sourcing records.

Validates one or many sourcing records against schema.json (a JSON-Schema subset) plus a
few "completeness gate" lint rules that schema alone can't express. Zero external
dependencies (pure stdlib); if `jsonschema` happens to be installed it is NOT required.

Usage:
    python validate.py <file.json>          # a single record OR a JSON array of records
    python validate.py <directory>          # validates every *.json under it (recursively)
    python validate.py --self-test          # validate the bundled golden cases

Exit code 0 = all records valid; 1 = at least one failure (CI-friendly).
"""
import json
import os
import sys
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(HERE, "..", "schema.json")
GOLDEN_DIR = os.path.join(HERE, "..", "tests", "golden")

VAGUE_LEVERS = {"buy in bulk", "shop around", "negotiate", "buy more", "go wholesale"}


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ---- minimal JSON-Schema (draft-07 subset) validator -----------------------------------

def _type_ok(value, t):
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    return True


def validate_node(value, schema, path, errors):
    t = schema.get("type")
    if t and not _type_ok(value, t):
        errors.append(f"{path}: expected type '{t}', got {type(value).__name__}")
        return  # type wrong -> downstream checks meaningless

    if t == "object":
        for req in schema.get("required", []):
            if req not in value:
                errors.append(f"{path}: missing required field '{req}'")
        props = schema.get("properties", {})
        for key, subschema in props.items():
            if key in value:
                validate_node(value[key], subschema, f"{path}.{key}", errors)

    elif t == "array":
        min_items = schema.get("minItems")
        if min_items is not None and len(value) < min_items:
            errors.append(f"{path}: needs >= {min_items} item(s), found {len(value)}")
        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(value):
                validate_node(item, item_schema, f"{path}[{i}]", errors)

    elif t == "string":
        ml = schema.get("minLength")
        if ml is not None and len(value) < ml:
            errors.append(f"{path}: string shorter than minLength {ml} (got '{value}')")

    elif t == "number":
        mn = schema.get("minimum")
        if mn is not None and value < mn:
            errors.append(f"{path}: {value} below minimum {mn}")

    enum = schema.get("enum")
    if enum is not None and value not in enum:
        errors.append(f"{path}: '{value}' not in allowed values {enum}")


# ---- completeness-gate lint rules (beyond raw schema) ----------------------------------

def lint_record(rec, path, errors):
    lever = (rec.get("lever") or "").strip().lower()
    if lever in VAGUE_LEVERS:
        errors.append(f"{path}.lever: too vague ('{lever}') — name the specific change")

    floor = rec.get("floor", {})
    sc = rec.get("supply_chain", {})
    if floor.get("already_at_floor") is True and sc.get("next_tier") != "already_at_floor":
        errors.append(
            f"{path}: floor.already_at_floor is true but supply_chain.next_tier is "
            f"'{sc.get('next_tier')}' (expected 'already_at_floor')"
        )

    for i, sup in enumerate(rec.get("recommended_suppliers", [])):
        if not (sup.get("moq") or "").strip():
            errors.append(f"{path}.recommended_suppliers[{i}]: missing MOQ")

    # Freight/cold-chain is a quality-gate item — a blank note is not "checked".
    if "freight_risk" in rec and not (rec.get("freight_risk") or "").strip():
        errors.append(f"{path}.freight_risk: blank — state the freight/cold-chain reality (use 'low'/'n/a' if none)")


def validate_record(rec, schema, path):
    errors = []
    validate_node(rec, schema, path, errors)
    lint_record(rec, path, errors)
    return errors


# ---- driver ----------------------------------------------------------------------------

def _records_from_file(fp):
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]


def _iter_inputs(target):
    if os.path.isdir(target):
        for fp in sorted(glob.glob(os.path.join(target, "**", "*.json"), recursive=True)):
            yield fp
    else:
        yield target


def run(target):
    schema = load_schema()
    total = passed = 0
    any_fail = False
    for fp in _iter_inputs(target):
        try:
            records = _records_from_file(fp)
        except Exception as e:  # noqa: BLE001
            print(f"FAIL  {fp}: could not parse JSON ({e})")
            any_fail = True
            continue
        for idx, rec in enumerate(records):
            total += 1
            label = f"{os.path.basename(fp)}[{idx}]" if len(records) > 1 else os.path.basename(fp)
            errs = validate_record(rec, schema, rec.get("ingredient", label))
            if errs:
                any_fail = True
                print(f"FAIL  {label}  ({rec.get('ingredient', '?')})")
                for e in errs:
                    print(f"        - {e}")
            else:
                passed += 1
                print(f"PASS  {label}  ({rec.get('ingredient', '?')})")
    print(f"\n{passed}/{total} record(s) valid.")
    return 1 if any_fail else 0


def self_test():
    print(f"Self-test: validating golden cases in {os.path.relpath(GOLDEN_DIR, HERE)}\n")
    return run(GOLDEN_DIR)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    arg = sys.argv[1]
    sys.exit(self_test() if arg == "--self-test" else run(arg))
