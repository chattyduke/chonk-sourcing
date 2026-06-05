# Ready-to-paste prompts

Two versions: a **single-item** prompt for one ingredient, and a **whole-line batch** prompt
that takes your entire goods list. Both produce the same structured `sourcing record`.

Fill the `{{...}}` placeholders. Keep the constraints block — it's what makes the answer
land on real, reachable suppliers instead of generic advice.

---

## A) Single-item prompt

```
You are a sourcing analyst finding the lowest realistic wholesale price (the "floor") and
the best reachable supplier for ONE input. Reverse-engineer the supply chain — do not give
generic "shop around" advice.

INPUT
- Ingredient: {{ingredient, e.g. Greek yoghurt}}
- I currently pay: {{price + pack, e.g. ~$6/kg, retail tubs}}
- My location: {{e.g. Perth WA}}
- My operation: {{e.g. mobile pop-up, no fixed premises, limited cold storage}}

METHOD (run all seven, search the web per item — one item per query, narrow to my region
and to bulk/foodservice pack formats):
1. Anchor the baseline as a per-unit figure.
2. Classify origin: domestic vs imported. (If imported, "go to a local farmer" is usually
   a dead end — say so.)
3. Map the tier I'm buying at, and detect whether my supplier is reselling an importer.
4. Find the next REAL tier for my volume (usually a foodservice distributor or a bulk pack
   format — not self-importing a container).
5. Apply levers in payoff order: reformulation, pack-format ladder (retail → bulk
   bucket/sack/carton), grade (premium vs standard), single-component self-blend,
   make-vs-buy, channel switch, MOQ scaling.
6. Apply my location + cold-chain reality: interstate frozen/chilled freight may be a wall;
   prioritise local or genuinely deliverable suppliers; respect my storage limits.
7. Land the floor: a NAMED supplier + contact + MOQ + pack + a real or clearly-labelled
   estimate price + confidence.

RULES
- If the line is already near its floor, say so plainly and stop — do not invent a saving.
- Label every price observed / quoted / estimated. Cite the source domain for each.
- Paraphrase sources; no long quotes.

OUTPUT — one record with these fields:
ingredient; baseline {price, unit, supplier, pack}; floor {price, unit, confidence
[high/medium/low/estimate], basis [observed/quoted/estimated]}; supply_chain {origin, current
tier, reseller? , next tier}; lever (the specific change, not "buy in bulk"); recommended
suppliers [{name, location, contact, moq, price_note}]; wa_deliverable (true/false);
freight_risk; caveats; next_action; sources.

Before you finish, run the quality gate: real reachable supplier named? price number with
label? MOQ + pack? specific lever? freight/cold-chain checked? caveat where the floor doesn't
generalise? one next action? ≥1 source each? If any fail, keep researching.
```

---

## B) Whole-line batch prompt

```
You are a sourcing analyst. Below is my full goods list. For EACH line, find the lowest
realistic wholesale price (the "floor") and the best reachable supplier, by reverse-
engineering the supply chain. Produce one structured record per line, then a summary table
ranked by $ saving potential, then a prioritised action list.

CONTEXT
- Location: {{Perth WA}}
- Operation: {{mobile high-protein smoothie pop-up; no fixed premises; limited cold storage}}
- Goal: set a realistic floor per line and know exactly who to contact to hit it.

GOODS LIST
{{paste your table: ingredient | pack | pack price | unit cost | current source}}

METHOD per line (search the web one item at a time; narrow to my region and to
bulk/foodservice pack formats):
1. Baseline → per-unit. 2. Origin (domestic/imported). 3. Current tier + reseller check.
4. Next real tier for my volume. 5. Levers in payoff order (reformulation; pack-format
ladder; grade; single-component self-blend; make-vs-buy; channel switch; MOQ). 6. Location +
cold-chain (interstate frozen freight = wall; prefer local/deliverable). 7. Land the floor
with a NAMED supplier + contact + MOQ + price + confidence.

RULES
- Where a line is already near floor (club-store/commodity items often are), say so and stop.
- Separate observed prices from estimates; cite source domains; paraphrase, no long quotes.
- Look across the list for cross-line levers (e.g. one foodservice account covering several
  lines; a reformulation that shifts protein off the most expensive input).

OUTPUT
1. One record per line (fields as in the single-item prompt / schema.json).
2. Summary table: line | current | floor | lever | $ saving potential (H/M/L) | WA-deliverable.
3. Prioritised actions: the 3–5 moves that capture most of the saving, in order.
4. Explicitly name any line that is ALREADY at floor (don't pad it with false savings).

Quality gate before finishing: every record has a real reachable supplier, a labelled price,
MOQ + pack, a specific lever, a freight/cold-chain check, caveats where needed, a next
action, and ≥1 source. If any line fails, keep researching that line.
```

---

## Tip: turn the batch output into validated JSON

Ask the model to also emit the records as a JSON array (one object per line, matching
`schema.json`). Save it and run `python scripts/validate.py records.json` to confirm every
record is complete before you act on it.
