---
name: chonk-sourcing
description: Find the lowest realistic wholesale price (the "floor") and the best reachable supplier for any physical ingredient, packaging item, or commodity input, by reverse-engineering its supply chain. Use this WHENEVER the user wants to source an ingredient cheaper, lower a COGS line, find a wholesale or bulk supplier, "go direct", bypass a middleman, benchmark what they pay, or asks "how low can we go" / "who else supplies X" / "is there a cheaper source for X". Triggers on any mention of supplier, sourcing, wholesale, bulk pricing, foodservice, distributor, importer, "price per kg/L/unit", COGS, ingredient cost, or procurement for a small/mobile food business. Built for a Perth WA mobile pop-up (chonk.) but works for any location and input. Prioritises completeness, real named suppliers with contacts and MOQs, and an evidence-backed price floor — never a vague "shop around".
---

# chonk-sourcing — Supply-Chain Floor Finder

## What this skill does

Given an ingredient and what the user currently pays, this skill produces a structured
**sourcing record**: the realistic price *floor*, the named supplier(s) that hit it, their
contact details and minimum order, the specific *lever* that unlocks the saving, and one
concrete next action. It does this by tearing down the supply chain rather than guessing.

The core insight it encodes: **the cheapest tier is rarely where intuition points.** "Go
direct to a farmer" is usually a dead end (domestic frozen/processed inputs cost *more* than
imports); the real floor sits at a pack-format change, a grade change, a recipe change, or
one tier up the import chain — and for a remote market like Perth WA, **freight and cold
chain set a hard local floor** that east-coast "sources" can't beat.

## When to use it (and when not)

USE for any physical input the user buys and wants cheaper: ingredients, packaging,
consumables. USE when turning a whole goods/COGS list into a sourcing plan (batch mode).

DO NOT use for: choosing between suppliers the user already has on equal terms (that's
vendor scoring — see `references/adjacent-skills.md`), contract/legal review, or
non-physical/SaaS spend.

## The method (summary)

Run all seven steps for each input. Full detail and heuristics:
**read `references/methodology.md`.** WA/Perth supplier leads and the price ladder:
**read `references/wa-supplier-map.md`.**

1. **Anchor the baseline** — current price, unit, supplier, pack format. Normalise to a
   per-unit figure ($/kg, $/L, $/unit) so tiers are comparable.
2. **Classify origin** — domestic vs imported vs mixed. This decides whether "direct to
   grower" is even viable. Most frozen/processed inputs in AU are imported; domestic-grown
   frozen usually costs *more*, not less.
3. **Map the current tier + detect reseller** — is the current "wholesaler" actually
   reselling an importer? (Tell-tales: a regional distributor whose brands belong to a
   national importer; an importer who "services your state through a distributor".) The
   margin to bypass is real, but the tier above may loop back to where you started.
4. **Find the next *real* tier** — retail → regional distributor → foodservice distributor
   → importer → manufacturer/grower. Name the realistic one for this buyer's volume, not a
   fantasy tier requiring container MOQs they can't absorb.
5. **Apply the product-specific levers** (the highest-value step):
   - **Pack-format ladder** — retail tub/bottle → bulk bucket/sack/carton (e.g. yoghurt
     retail $6/kg → 10kg foodservice bucket ~$3.80/kg).
   - **Grade** — premium positioning vs standard (e.g. "raw cacao" vs standard cocoa).
   - **Composition** — buy single-component and self-blend instead of a pre-mix; the blend
     hides cheap vs expensive components.
   - **Reformulation** — don't source a spec (e.g. "50g protein") entirely from the most
     expensive input; let cheaper inputs (milk, yoghurt, PB) contribute.
6. **Apply location + logistics reality** — for remote markets (Perth WA), frozen/chilled
   freight from interstate is a wall ($250–500/drop). Prioritise local or genuinely
   deliverable suppliers; respect cold-chain limits for mobile operators (no fixed
   premises, dispenser/chiller constraints).
7. **Land the floor** — a *named* supplier + contact + MOQ + pack + a real or clearly
   labelled-estimate price + confidence level. Then one concrete next action.

## How to research (tooling)

- Use web search/fetch. Search **per item**, not combined queries — one input at a time
  gets real prices; combined queries return surface-level results for all.
- Start broad (the commodity + "wholesale"/"foodservice"/"bulk 10kg"), then narrow to the
  buyer's region and pack format.
- Prefer trade/foodservice catalogues, distributor sites, and importer pages over retail
  aggregators. Many show price only after login — capture the pack format + MOQ even when
  the number is gated, and label the price an estimate.
- Confirm WA-deliverability explicitly. "Delivers nationwide" often means "via a state
  distributor" — verify, because that changes the floor.
- **Citations + copyright:** paraphrase; cite the source domain for any price/claim; never
  paste long passages. A price figure is a fact — attribute it, don't quote surrounding text.

## Output contract

Emit one **sourcing record** per ingredient, conforming to `schema.json`. In chat, render
it as a compact block; when batching a whole list, also write the records as JSON so they
validate (see below). Minimum every record MUST contain: baseline (price+unit), floor
(price+confidence+`basis` label observed/quoted/estimated), current tier + next tier, the
lever, ≥1 named recommended supplier with an MOQ, WA-deliverability flag, a freight/cold-chain
note, ≥1 source, and a next action. See `PROMPT.md` for the ready-to-paste prompts
(single-item and whole-line batch).

## Quality gate — run this before shipping any record

Do not output a record (or claim a line is "done") until every box is ticked. If one fails,
keep researching — completeness is the product.

- [ ] Named a **real supplier reachable from the buyer's location** (not "an importer").
- [ ] Have a **price number** for the floor, labelled `observed` / `quoted` / `estimated`.
- [ ] Captured **MOQ + pack format**.
- [ ] Stated the **specific lever** (not "buy in bulk" — *which* pack/grade/recipe change).
- [ ] Checked **freight + cold chain** for this location/operator.
- [ ] Flagged any **caveat** where the floor doesn't generalise (e.g. the dairy floor does
      not apply to coconut yoghurt).
- [ ] Gave **one concrete next action**.
- [ ] Cited **≥1 source** per price/claim.

Then optionally validate the JSON: `python scripts/validate.py <record-or-dir>` (see README).

## Honesty rules

- If a line is **already near its floor**, say so plainly and stop — don't manufacture a
  saving. (Costco often beats a regional "wholesale" price; milk barely compresses below
  ~$1.40/L.) A correct "you're already there" is a complete answer.
- Separate **observed** prices from **estimates**; never present an estimate as a quote.
- A "send to council/regulator" list is a **traceability** document — ingredient + supplier
  + location only, never pricing. Keep cost analysis in a separate internal artifact.
