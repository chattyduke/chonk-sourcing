# The Supply-Chain Floor Method (full reference)

This is the detailed version of the seven-step method in SKILL.md. Read it when you need the
heuristics, the failure modes to avoid, and worked patterns.

## Contents
1. Step-by-step with heuristics
2. The price ladder (mental model)
3. Lever catalogue (ranked by typical payoff)
4. Reseller-detection tells
5. Location & cold-chain rules
6. Failure modes (what NOT to do)
7. Worked examples

---

## 1. Step-by-step with heuristics

### Step 1 — Anchor the baseline
Normalise everything to a single per-unit number: `$/kg`, `$/L`, or `$/unit`. Convert pack
prices (e.g. "$15–18 for 2kg" → "$8.25/kg"). Record the *channel* you're buying through
(retail, club store, regional distributor) — that, not the brand, sets the tier.

### Step 2 — Classify origin
Ask: is this grown/made domestically or imported? Decision rule:
- **Imported** (most frozen berries, frozen tropical fruit, cocoa, coconut water,
  commodity whey): the floor lives in the import chain. "Go to a local farmer" will be
  *dearer*, because local produce sells fresh at a premium and isn't frozen at scale.
- **Domestic** (milk, honey, oats, banana, dairy yoghurt): a local manufacturer/dairy or
  the central produce market is a viable tier; freight is less of a wall.

### Step 3 — Map current tier + detect reseller
Place the current supplier on the ladder (Section 2). Then check whether they're reselling
someone upstream (Section 4 tells). If yes, the *next* tier may just be their wholesaler —
which, after freight, can be no cheaper. This is the single most common reason a "bypass the
middleman" hunt disappoints.

### Step 4 — Find the next real tier
Pick the realistic tier for this buyer's volume:
- Small/mobile operator ($50–150k revenue): the next tier is almost always a **foodservice
  distributor account** (one-stop, no container MOQ) or a **bulk pack format** from the same
  channel — not self-importing.
- Self-import (container/pallet, FCL/LCL) only pencils out at tonnes/month with own cold
  storage, customs and biosecurity capability. Flag it as the theoretical floor, not the
  actionable one, unless the buyer is at that scale.

### Step 5 — Apply levers
See Section 3. Work them in payoff order; usually the recipe/pack levers beat hunting a
cheaper supplier of the same item.

### Step 6 — Location & logistics
See Section 5. For Perth WA specifically: interstate frozen/chilled freight is a wall;
prioritise WA-local or WA-deliverable suppliers (`references/wa-supplier-map.md`).

### Step 7 — Land the floor
Produce the record per `schema.json`. A floor without a named, reachable supplier + MOQ is
not a floor — it's a rumour. Label estimates as estimates.

---

## 2. The price ladder (mental model)

From most expensive to cheapest, roughly:

```
Retail / grocery
  → Club store (Costco)            ← often already at/below regional "wholesale"
    → Regional distributor          ← may be a reseller of an importer
      → Foodservice distributor      ← best one-stop tier for small operators
        → Importer / national wholesaler
          → Manufacturer / packer direct
            → Self-import (container)  ← theoretical floor; needs scale + infrastructure
```

Two ladder truths that surprise people:
- **Club-store pricing (Costco) is frequently at or below a regional distributor's "trade"
  price** on commodity lines (milk, frozen berries, coconut water, honey, oats). Verify
  before assuming "wholesale = cheaper".
- **Each rung down adds operational cost** (MOQ, storage, handling, freight). The cheapest
  per-unit rung is not the cheapest *all-in* rung for a small buyer.

---

## 3. Lever catalogue (ranked by typical payoff)

1. **Reformulation** — stop sourcing an expensive spec from the single priciest input.
   *Example:* a "50g protein" shake doesn't need all 50g from whey; milk (~8g/250ml), Greek
   yoghurt (~9–10g/100g) and peanut butter (~7.5g/30g) can contribute ~20–25g, cutting whey
   per serve materially while the claim stays true. Often the biggest COGS win on a list.
2. **Pack-format ladder** — retail → bulk. *Example:* Greek yoghurt retail ~$6/kg →
   10kg foodservice bucket ~$3.80/kg (~37% off). Whey retail per-scoop → 20kg sack.
3. **Grade / positioning** — premium label vs standard. *Example:* "raw cacao" carries a
   premium; standard foodservice cocoa is much cheaper if the brand permits.
4. **Composition / self-blend** — buy single-component IQF and blend in-house instead of a
   pre-mix; you control the ratio and skip the blend premium.
5. **Make vs buy convenience** — *Example:* branded frozen banana chunks ~$10.50/kg vs
   freezing fresh banana (~$2.50/kg) or IQF banana from an importer (~$4–6/kg).
6. **Channel switch** — open a foodservice trade account (tailored pricing) vs paying
   retail/club shelf price; or buy fresh produce at the central market vs grocery.
7. **MOQ scaling** — for packaging/custom print, go factory-direct at higher MOQ.

---

## 4. Reseller-detection tells

A current supplier is probably reselling someone upstream when:
- Their product range is dominated by **another company's brands** (the brand owner is the
  real importer).
- Their socials/handle pair their name with a **national brand** ("X WA / BrandHQ").
- A national importer's site says it **"services your state through a distributor"** or
  routes your-region enquiries to a partner.
- They won't quote trade pricing until you "start ordering" — a sign of a thin reseller
  margin they don't want benchmarked.

When detected: going "direct" to the upstream importer often routes you back to the same
regional reseller, plus interstate freight. The better move is to negotiate volume/pickup
pricing with the local arm, or switch to a broad-range foodservice distributor.

---

## 5. Location & cold-chain rules

- **Freight wall:** interstate frozen/chilled freight to remote markets (e.g. Perth) runs
  ~$250–500 per drop and breaks the cold-chain economics. An interstate "cheaper" per-unit
  price frequently loses to a local one after freight.
- **Prioritise local / deliverable:** confirm the supplier delivers to the region *directly*
  (own trucks/depot) rather than "nationwide via a distributor".
- **Local pickup** from a local importer/distributor strips their delivery margin — ask for
  a pickup rate.
- **Mobile-operator constraints:** no fixed premises = limited freezer/fridge; bag-in-box
  dispenser formats (e.g. milk pergal) save per-unit but need a dispenser/chiller and have
  short post-open windows (~48h) — often impractical for a trailer. Weigh the saving vs the
  operational fit, and say so.

---

## 6. Failure modes (what NOT to do)

- **Chasing a fantasy tier** ("find a farmer", "import a container") for a buyer who can't
  absorb the MOQ or logistics.
- **Combined search queries** ("cheap berries oats milk wholesale") — returns shallow
  results. One item per search.
- **Presenting an estimate as a quote.** Label `observed` vs `estimated`.
- **Manufacturing a saving on a line that's already at floor.** Say "already near floor" and
  move on — it's a complete, honest answer.
- **Ignoring all-in cost** — a lower per-unit price with high MOQ/freight/spoilage can be
  dearer in practice for a small operator.
- **Putting prices in a regulator/council list** — that document is traceability only.

---

## 7. Worked examples (abbreviated)

| Input | Baseline | Floor | Lever | Note |
|---|---|---|---|---|
| Greek yoghurt | ~$6/kg retail | ~$3.80/kg | 10kg foodservice bucket | Coconut yoghurt does NOT follow |
| Frozen banana (branded) | ~$10.50/kg | ~$2.50–5/kg | Freeze fresh, or IQF from importer | Easy win |
| Whey (WPC) | ~$31.7/kg | ~$30–34/kg | Already near floor → reformulate instead | Don't chase a cheaper whey |
| Mixed berries | ~$8.25/kg (club) | ~$7–9/kg | Already near floor; single-fruit self-blend only edge | Club beats regional "wholesale" |
| Milk | ~$1.43/L (club) | ~$1.30–1.60/L | Near floor; pergal saves marginally | Impractical for mobile |

The pattern: the wins concentrate in reformulation, pack format, and make-vs-buy — not in
finding a cheaper seller of the identical item.
