#!/usr/bin/env python3
"""
test_validate.py — positive + negative tests for the chonk-sourcing validator.

Runnable with no test framework:  python tests/test_validate.py
(Also discoverable by pytest if installed.)

Positive: every bundled golden record validates clean.
Negative: deliberately broken records produce the expected errors (proves the gate bites).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
GOLDEN = os.path.join(HERE, "golden")
sys.path.insert(0, SCRIPTS)

import validate  # noqa: E402  (from scripts/validate.py)

SCHEMA = validate.load_schema()


def _check(rec):
    return validate.validate_record(rec, SCHEMA, rec.get("ingredient", "rec"))


def test_golden_cases_all_pass():
    files = [f for f in os.listdir(GOLDEN) if f.endswith(".json")]
    assert files, "no golden cases found"
    for fn in sorted(files):
        with open(os.path.join(GOLDEN, fn), "r", encoding="utf-8") as f:
            rec = json.load(f)
        errs = _check(rec)
        assert errs == [], f"{fn} should be valid but got: {errs}"


def test_missing_required_field_fails():
    rec = {"ingredient": "Test"}  # almost everything missing
    errs = _check(rec)
    assert any("missing required field 'baseline'" in e for e in errs), errs
    assert any("missing required field 'sources'" in e for e in errs), errs


def test_bad_enum_fails():
    rec = json.load(open(os.path.join(GOLDEN, "yoghurt.json"), encoding="utf-8"))
    rec["floor"]["confidence"] = "very-sure"  # not in enum
    errs = _check(rec)
    assert any("not in allowed values" in e for e in errs), errs


def test_vague_lever_fails():
    rec = json.load(open(os.path.join(GOLDEN, "yoghurt.json"), encoding="utf-8"))
    rec["lever"] = "buy in bulk"
    errs = _check(rec)
    assert any("too vague" in e for e in errs), errs


def test_supplier_without_moq_fails():
    rec = json.load(open(os.path.join(GOLDEN, "yoghurt.json"), encoding="utf-8"))
    rec["recommended_suppliers"][0].pop("moq")
    errs = _check(rec)
    assert any("missing required field 'moq'" in e or "missing MOQ" in e for e in errs), errs


def test_empty_sources_fails():
    rec = json.load(open(os.path.join(GOLDEN, "yoghurt.json"), encoding="utf-8"))
    rec["sources"] = []
    errs = _check(rec)
    assert any("sources" in e and ">= 1" in e for e in errs), errs


def test_at_floor_consistency_rule():
    rec = json.load(open(os.path.join(GOLDEN, "wpc.json"), encoding="utf-8"))
    rec["supply_chain"]["next_tier"] = "importer"  # contradicts already_at_floor=true
    errs = _check(rec)
    assert any("already_at_floor is true" in e for e in errs), errs


def test_missing_floor_basis_fails():
    # Honesty rule: every floor price MUST carry an observed/quoted/estimated label.
    # SKILL.md ("never present an estimate as a quote") + PROMPT.md + README all promise it.
    rec = json.load(open(os.path.join(GOLDEN, "yoghurt.json"), encoding="utf-8"))
    rec["floor"].pop("basis")
    errs = _check(rec)
    assert any("missing required field 'basis'" in e for e in errs), errs


def test_missing_freight_risk_fails():
    # Quality-gate item: "Checked freight + cold chain for this location/operator."
    rec = json.load(open(os.path.join(GOLDEN, "yoghurt.json"), encoding="utf-8"))
    rec.pop("freight_risk")
    errs = _check(rec)
    assert any("missing required field 'freight_risk'" in e for e in errs), errs


def test_blank_freight_risk_fails():
    # An empty/whitespace freight note is not "checked" — the gate must bite.
    rec = json.load(open(os.path.join(GOLDEN, "yoghurt.json"), encoding="utf-8"))
    rec["freight_risk"] = "   "
    errs = _check(rec)
    assert any("freight_risk" in e and ("blank" in e or "empty" in e) for e in errs), errs


def _main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok    {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_main())
