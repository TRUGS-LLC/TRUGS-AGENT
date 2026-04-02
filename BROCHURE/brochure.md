# TRUGS Brochure — 11x17 Folded to 8.5x11

Layout: 4 panels. Print double-sided on 11x17, fold in half.

```
Outside (face up):  PANEL 4 (back)  |  PANEL 1 (front)
Inside (open):      PANEL 2 (left)  |  PANEL 3 (right)
```

---

# PANEL 1 — Front Cover

---

## TRUGS — Traceable Recursive Universal Graph Specification

```
<trl>
NAMESPACE TRUGS GOVERNS ALL DATA graph AND ALL RECORD sentence.
INTERFACE TRL CONTAINS 190 UNIQUE RECORD word.
EACH RECORD sentence SHALL COMPILE TO DATA graph.
EACH DATA graph SHALL COMPILE TO RECORD sentence.
AGENT SHALL READ RECORD sentence THEN EXECUTE.
NO AGENT SHALL GUESS RECORD meaning —
  EACH RECORD word HAS EXACTLY A RECORD definition.
</trl>
```

```json
{
  "nodes": [
    {"id": "trugs",      "type": "NAMESPACE", "properties": {"name": "TRUGS"}},
    {"id": "trl",        "type": "INTERFACE", "properties": {"name": "TRL", "words": 190}},
    {"id": "graph",      "type": "DATA",      "properties": {"name": "graph"}},
    {"id": "sentence",   "type": "RECORD",    "properties": {"name": "sentence"}},
    {"id": "agent",      "type": "AGENT",     "properties": {"name": "agent"}},
    {"id": "word",       "type": "RECORD",    "properties": {"unique": true}},
    {"id": "definition", "type": "RECORD",    "properties": {"name": "definition"}}
  ],
  "edges": [
    {"from_id": "trugs",    "to_id": "graph",      "relation": "GOVERNS"},
    {"from_id": "trugs",    "to_id": "sentence",   "relation": "GOVERNS"},
    {"from_id": "trl",      "to_id": "word",        "relation": "CONTAINS"},
    {"from_id": "sentence", "to_id": "graph",       "relation": "COMPILES_TO"},
    {"from_id": "graph",    "to_id": "sentence",    "relation": "COMPILES_TO"},
    {"from_id": "agent",    "to_id": "sentence",    "relation": "READS"},
    {"from_id": "word",     "to_id": "definition",  "relation": "HAS"}
  ]
}
```

Same specification. Same structure. Different views.
**The sentence is the graph. The graph is the sentence.**

---

# PANEL 2 — Inside Left: The Language

---

## The Problem You Already Know

Your prompts are ambiguous. "Make sure the code is clean" means something different every time. Your agent drifts from instructions mid-conversation. Your agent ships code it never audited against the spec. There is no spec — just English that everyone interprets differently.

## TRL — 190 Words That Don't Drift

TRL is a formal subset of English — 190 words drawn from computation and law. Every word has exactly one meaning. Every valid sentence compiles to a directed graph. Every graph decompiles back to a sentence. Losslessly.

**English:**

> Make sure users are authenticated before they can access data.
> Handle errors gracefully. Don't log passwords.

**TRL:**

```
<trl>
SERVICE api SHALL AUTHENTICATE PARTY user
  THEN READ DATA FROM STREAM database
  THEN WRITE RESULT TO PARTY user
  OR THROW EXCEPTION.
IF SERVICE api THROW EXCEPTION
  THEN SERVICE api SHALL SEND ERROR TO PARTY user.
NO SERVICE SHALL WRITE DATA credential TO STREAM log.
</trl>
```

The English is three suggestions. The TRL is seven executable obligations. SHALL means must. SHALL_NOT means must not. MAY means allowed. There is no "try" — only obligations, permissions, and prohibitions.

## The Validator

16 rules enforce graph correctness. 9 structural rules (always). 7 compositional rules (opt-in). Subject-operation compatibility. Modifier-entity constraints. No double negation. Reference scope resolution.

Your agent doesn't interpret TRL. It compiles it, validates it, and executes it. If the graph is invalid, the validator catches it before the agent acts.

**8 parts of speech. 190 words. Zero ambiguity.**

---

# PANEL 3 — Inside Right: The System

---

## Seven Components — Adopt One or All

```
research → plan → track → graph → specify → deliver → remember → index
```

| Component | What It Does |
|-----------|-------------|
| **FOLDER** | JSON graph indexes your filesystem — agent navigates without reading every file |
| **AAA** | 9-phase protocol — plan before code, define audit criteria before build, human approves at 3 gates |
| **EPIC** | Portfolio tracker as a traversable graph — what's blocked, what depends on what |
| **MEMORY** | 4-type persistence across sessions — decisions, preferences, project state, external references |
| **TRUGGING** | 4-level codebase description — system graph, folder graph, file header TRL, inline TRL |
| **WEB_HUB** | Curated web resources as a weighted graph — traverse research instead of searching |

Each component is one folder with a README (for you) and an AGENT.md (for your LLM). Copy what you need.

## Proof: It Works Outside Code

We built a mutual NDA — a legal document, not software — using all seven systems.

The graph has **23 nodes** (12 clauses + 11 bibliography references) and **26 edges** (clause dependencies + legal citations). Every obligation compiles to TRL:

```
<trl>
PARTY receiving SHALL PROTECT RECORD confidential_info
  WITH REASONABLE RECORD measures.
PARTY receiving SHALL_NOT DISCLOSE RECORD confidential_info
  TO ANY PARTY EXCEPT RECORD authorized_representative.
</trl>
```

Washington State law. RCW 19.108. King County jurisdiction. 12 sections. Signable document. The specification works for any structured domain — code, law, business, research, writing.

## Build On It

TRUGS is a specification, not a product. Define your domain's vocabulary. Validate against CORE. Build tools that read, write, and execute TRUGs in any language.

**Apache 2.0. No permission needed.**

---

# PANEL 4 — Back Cover: Get It

---

## Repositories

**TRUGS-AGENT** — The implementation guide
`github.com/TRUGS-LLC/TRUGS-AGENT`
[ QR CODE ]

**TRUGS** — The specification
`github.com/TRUGS-LLC/TRUGS`
[ QR CODE ]

## Paper

`github.com/TRUGS-LLC/TRUGS/blob/main/PAPER/trugs.pdf`
DOI: 10.5281/zenodo.19379454

## Contact

admin@trugs.ai

## License

Apache 2.0 — TRUGS LLC — Seattle, WA
