# Adjacent skills (ecosystem scan, Jun 2026)

Scan of public Claude/Claude Code skills for "find the cheapest supplier / price floor for a
physical input". Finding: **no existing skill does this exact job.** The closest are listed
below — use them *alongside* chonk-sourcing, not instead of it.

## General research engines (the layer underneath)

- **Weizhena/Deep-Research-skills** — structured, human-in-the-loop deep research for Claude
  Code / OpenCode / Codex; uses Exa web search + `pyyaml`. A solid general research engine to
  run *under* chonk-sourcing's method. No sourcing logic of its own.
- **daymade/claude-code-skills** — includes a `deep-research` skill and `competitors-analysis`
  (evidence-sourced). Good for broad investigation; not commodity sourcing.
- **web-research-task pattern** — spawns a background agent that drives Claude.ai's Research
  toggle and writes results to a markdown file. Useful harness; no sourcing method.

## Enterprise procurement packs (use *after* candidates exist)

- **vendor-evaluation**, **supplier-scorecard** (in `w95/awesome-claude-corporate-skills`) —
  score/compare suppliers you already have. Natural follow-on once chonk-sourcing has
  surfaced 2–3 candidates per line.
- **procurement-optimizer**, **vendor-management** (in `alirezarezvani/claude-skills`) —
  spend optimisation / relationship management.
- **rfp-builder**, **contract-negotiation**, **inventory-forecasting** — RFP and contract
  workflows; relevant only at larger scale.
- **energy-procurement** (`affaan-m/everything-claude-code`) — domain-specific (electricity
  tariffs); cited as an example of how deep a single-domain procurement skill can go.

## Official

- **anthropics/skills** — `skill-creator`, `template-skill`, and the document skills
  (docx/pdf/pptx/xlsx). `skill-creator` is what you'd use to iterate/optimise this skill's
  triggering and run evals.

## Recommended stack for chonk.

1. A deep-research skill (Weizhena or daymade) as the search engine.
2. **chonk-sourcing** (this skill) for the sourcing method + floor + output contract.
3. `vendor-evaluation` / `supplier-scorecard` once you're choosing between real quotes.
