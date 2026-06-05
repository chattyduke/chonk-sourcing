# chonk-sourcing

Find the **lowest realistic wholesale price (the "floor")** and the **best reachable
supplier** for any physical ingredient, packaging item, or commodity input — by
reverse-engineering its supply chain, not by guessing.

Built from the live chonk. sourcing work (the Greek-yoghurt teardown that took a $6/kg
retail line down to a ~$3.80/kg 10kg foodservice bucket). Generalises to the whole goods
list and to any location, but ships with Perth WA / mobile-pop-up defaults.

---

## Why this exists (the gap it fills)

A scan of the public Claude skill ecosystem (Jun 2026) found lots of *adjacent* tools but
nothing that does this job:

- **Deep-research engines** — `Weizhena/Deep-Research-skills`, `daymade/claude-code-skills`
  (deep-research), the `web-research-task` pattern. Great general researchers; no sourcing
  method, no supply-chain teardown, no price floor.
- **Enterprise procurement packs** — `vendor-evaluation`, `supplier-scorecard`,
  `procurement-optimizer`, `rfp-builder` (in `alirezarezvani/claude-skills`,
  `w95/awesome-claude-corporate-skills`), plus domain ones like `energy-procurement`. These
  **score or manage suppliers you already have**, or run RFPs — they assume the candidate
  set exists.

The missing piece, which this skill provides: *discover* the cheapest source for a specific
commodity input by tearing down the chain (reseller → importer → manufacturer), applying
pack-format / grade / composition / reformulation levers, and respecting real
location/cold-chain/freight constraints — ending on a named, reachable supplier with a
price, MOQ, and next action.

**Pairs well with:** a deep-research skill as the general search engine underneath, and
`vendor-evaluation` / `supplier-scorecard` *after* this skill has produced candidates.
See `references/adjacent-skills.md` for the full scan and the recommended stack.

---

## What's in the box

```
chonk-sourcing/
├── SKILL.md                     # the skill: method, output contract, quality gate
├── PROMPT.md                    # ready-to-paste prompts (single-item + whole-line batch)
├── schema.json                  # the sourcing-record output contract (JSON Schema draft-07)
├── README.md                    # this file
├── references/
│   ├── methodology.md           # full method, heuristics, lever catalogue, failure modes
│   └── wa-supplier-map.md       # warm Perth/WA leads, contacts, MOQs, the price ladder
├── scripts/
│   └── validate.py              # zero-dependency completeness checker / CI gate
└── tests/
    ├── test_validate.py         # positive + negative tests (7 cases)
    └── golden/                  # 4 worked records that must always validate
        ├── yoghurt.json
        ├── frozen-banana.json
        ├── wpc.json
        └── berries.json
```

---

## Install

**Claude Code** — drop the folder into your skills directory:

```bash
cp -r chonk-sourcing ~/.claude/skills/chonk-sourcing
```

Or install the packaged `chonk-sourcing.skill` via your skill manager / marketplace.

**Claude.ai (Pro/Max/Team/Enterprise, code execution on)** — upload the `.skill` file in
the Skills settings.

**Your Obsidian vault** — it's plain markdown + a tiny stdlib Python script; it lives
happily alongside `chonk-marketing`, `chonk-newsletter`, and `kepano-vault`. The skill body
references `methodology.md` and `wa-supplier-map.md` by relative path.

---

## Usage

**The fast path:** open `PROMPT.md`, copy the single-item or whole-line prompt, fill the
`{{...}}` blanks, paste. (You asked for "a prompt that finds this kind of supplier for the
whole product line" — the batch prompt in `PROMPT.md` is exactly that.)

**In an agent with the skill installed:** just ask in natural language —
"how low can I get peanut butter?", "find a cheaper yoghurt supplier", "run my whole goods
list for sourcing floors". The description triggers the skill; it runs the seven-step method
and emits one record per input.

**Output:** a structured `sourcing record` per input (see `schema.json`). In batch mode you
also get a summary table ranked by saving potential and a prioritised action list.

---

## Validate the output (the test)

The skill is only as good as the records it emits, so there's a runnable gate.

```bash
# validate a single record or a JSON array of records
python scripts/validate.py records.json

# validate a directory of records
python scripts/validate.py path/to/records/

# sanity-check the bundled golden cases
python scripts/validate.py --self-test
```

It checks each record against `schema.json` **plus** completeness lints schema can't express
(no vague levers like "buy in bulk"; every supplier has an MOQ; `already_at_floor` records
stay internally consistent). Exit code 0 = all valid, 1 = something's incomplete — so it
drops straight into CI or a pre-commit hook.

Run the test suite:

```bash
python tests/test_validate.py      # 10 tests: golden cases pass, broken records fail
```

Current status: **4/4 golden records valid, 10/10 tests passing.**

---

## The method in one paragraph

Anchor the baseline as a per-unit price → classify origin (domestic vs imported; "go to a
farmer" is usually a dead end for imported/processed inputs) → map your current tier and
detect whether your "wholesaler" is reselling an importer → find the next *real* tier for
your volume (usually a foodservice account or a bulk pack format, not self-importing) →
apply the levers that actually move COGS (reformulation, pack-format ladder, grade,
self-blend, make-vs-buy) → respect location and cold chain (interstate frozen freight is a
wall for Perth) → land on a named supplier with a contact, MOQ, price, and next action. Full
detail in `references/methodology.md`.

---

## Limitations & honesty

- **Prices drift.** Treat figures as benchmarks; the skill labels each `observed` / `quoted`
  / `estimated` and dates every record (`as_of`). Re-run before committing spend.
- **It will tell you when you're already at the floor** (club-store commodity lines often
  are) instead of inventing a saving. That's a feature.
- **Gated trade prices** sometimes can't be read without an account; the skill captures
  pack + MOQ and marks the price an estimate rather than fabricating one.
- **Not a regulator document.** A council/health "ingredient–supplier list" is traceability
  only (ingredient + supplier + location, no pricing) — keep cost analysis separate.

---

## Changelog

- **1.1.0** (2026-06-05) — honesty-gate hardening. The validator now **enforces** the skill's
  own quality-gate promises that were previously instruction-only: `floor.basis`
  (observed/quoted/estimated) is required, and `freight_risk` is required and must be non-blank.
  A record that omits the price-honesty label or the freight/cold-chain check now fails
  validation instead of silently passing. 3 new regression tests (10 total); all 4 golden
  records unchanged (they already carried both fields).
- **1.0.0** (2026-06-05) — initial release. Seven-step method, output schema, zero-dep
  validator, 4 golden cases, 7 tests, WA supplier map, single + batch prompts.
