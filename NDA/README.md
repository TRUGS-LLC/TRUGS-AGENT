# NDA — Non-Disclosure Agreement Example

A complete example showing every TRUGS-AGENT system applied to a non-code domain: drafting a mutual Non-Disclosure Agreement under Washington State law.

TRUGs aren't just for code. Any domain with structure — legal, business, writing, research — benefits from machine-readable graphs and formalized instructions. An NDA is a perfect example: clauses are nodes, obligations are TRL, dependencies are edges.

---

## How We Built This NDA — Step by Step

### Step 1: Research — WEB_HUB

Before writing anything, we built a research graph. `web.trug.json` indexes 20 curated web resources across four categories:

| Category | Resources | What They Provide |
|----------|-----------|-------------------|
| Templates | Bonterms, uNDA, eForms, NVCA, Open Agreements | Starting points — real NDA language to build from |
| Legal Guidance | ABA best practices, 8 essential provisions, enforceability | What clauses are required, what pitfalls to avoid |
| Tools | Lumin, Spellbook, AI Lawyer, QuickLegal | NDA generators and review tools for comparison |
| Statutes | RCW 19.108, DTSA, UTSA, Cornell LII | The law — what makes an NDA enforceable in WA |

**The web hub is a TRUG.** Each resource is a node with a URL, a one-sentence purpose, and weighted edges showing how resources relate. An LLM reads it to pull the right citations, find templates, or understand the legal landscape — without browsing.

### Step 2: Plan — AAA

With research done, we wrote the 9-phase AAA plan in `AAA_nda_draft.md`:

| Phase | What Happened |
|-------|--------------|
| 1. VISION | Human states what they want: mutual NDA, WA state, plain English, protect TRUGS IP |
| 2. FEASIBILITY | GO — WA has UTSA (RCW 19.108), DTSA provides federal layer, open-source templates exist |
| 3. SPECIFICATIONS | 12 required clauses defined in TRL, audit criteria written — "done" defined before drafting |
| 4. ARCHITECTURE | Document structure, design decisions (2yr term, 3yr survival, King County jurisdiction) |
| 5. VALIDATION | Human approves the plan before any drafting begins |
| 6. CODING | Draft each clause — TRL spec first, then plain English |
| 7. TESTING | Verify all 12 clauses present, all obligations mutual, all modals correct |
| 8. AUDIT | Check against Phase 3 criteria — 9 checks, all green |
| 9. DEPLOYMENT | Example complete — this is a demonstration, not a live deployment |

**Phase 3 defines the audit. Phase 8 executes against it.** The plan defines "done" before any writing starts.

### Step 3: Track — EPIC

The project tracker `epic.trug.json` breaks the work into 3 epics and 13 tasks with dependency edges:

```
Research & Planning
  ├── Research templates          ─┐
  ├── Review WA law (RCW 19.108)  ─┤── Write AAA plan
  └── Write AAA plan              ─┘

Draft NDA
  ├── Preamble & definitions      ─┐
  ├── Obligations                 ─┤── (depends on definitions)
  ├── Exclusions                  ─┤── (depends on definitions)
  ├── Term & termination          ─┤── (depends on obligations)
  ├── Remedies                    ─┤── (depends on obligations)
  ├── General provisions          ─┤── (depends on term)
  └── Whistleblower notice        ─┘

Review & Finalize
  ├── Audit against Phase 3       ── (after all clauses)
  ├── Verify TRL compiles         ── (after audit)
  └── Human review — HITM gate    ── (after all checks)
```

**BLOCKS edges enforce order.** You can't draft obligations before definitions. You can't audit before all clauses exist. You can't ship before human review.

### Step 4: Build the Graph — nda.trug.json

Before writing the document, we described the NDA as a TRUG graph. `nda.trug.json` has:

- **23 nodes:** 1 namespace (the NDA itself), 12 clause nodes, 11 bibliography reference nodes
- **26 edges:** 15 structural (DEPENDS_ON, GOVERNS between clauses) + 11 bibliographic (REFERENCES to sources)

Each clause node carries structured properties:

```json
{
  "id": "clause_definition",
  "type": "RECORD",
  "properties": {
    "name": "Section 3 — Definition of Confidential Information",
    "section": 3,
    "purpose": "Defines what information is protected...",
    "defines": ["Confidential Information"],
    "includes": ["source code", "specifications", "algorithms", ...]
  }
}
```

Edges show legal structure — the exclusions clause DEPENDS_ON the definition clause, the remedies clause DEPENDS_ON the obligations clause, the governing law REFERENCES RCW 19.108.

**The graph is the contract's skeleton.** An LLM reads it to understand clause relationships, find which sections reference which statutes, and verify completeness — without reading the full document.

### Step 5: Write with TRL — EXAMPLE_nda_mutual.md

Each clause is written twice: TRL specification first, then plain English.

```markdown
## 5. Obligations of the Receiving Party

<trl>
PARTY receiving SHALL PROTECT RECORD confidential_info WITH REASONABLE RECORD measures.
PARTY receiving SHALL USE RECORD confidential_info ONLY FOR RECORD Purpose.
PARTY receiving SHALL_NOT DISCLOSE RECORD confidential_info TO ANY PARTY
  EXCEPT RECORD authorized_representative WHO HAS RECORD obligation OF RECORD confidentiality.
</trl>

The Receiving Party shall:
(a) protect Confidential Information using at least the same degree of care...
```

**The TRL is the contract. The English is the explanation.** An LLM can verify the English matches the TRL, generate tests from the TRL, or detect when one changes but the other doesn't.

The bibliography at the end maps every source to the sections it informed.

### Step 6: Produce the Clean Document — NDA_mutual_trugs_llc.md

The final output: a clean, signable NDA with no TRL, no annotations, no graph references. Plain English, 12 sections, WA state jurisdiction.

This is what the counterparty sees. Everything else — the TRUG, the TRL, the research, the plan — is the machine-readable infrastructure that produced it.

### Step 7: Remember — MEMORY

Decisions from the drafting process are saved in `MEMORY.md`:
- **Jurisdiction:** WA state, King County, RCW 19.108
- **Term:** 2 years, 3-year survival for trade secrets
- **Style:** Plain English, no legalese, TRL for formal obligations
- **Template baseline:** Bonterms Mutual NDA

If we draft another agreement next session, the LLM already knows the jurisdiction, the style preference, and the legal references.

### Step 8: Index — folder.trug.json

Finally, `folder.trug.json` indexes all 10 files with edges showing the production pipeline:

```
nda.trug.json ──produces──→ EXAMPLE_nda_mutual.md ──produces──→ NDA_mutual_trugs_llc.md
     ↑                              ↑                                    ↑
  AAA governs               TRL annotations                    Clean output
```

An LLM entering this folder reads `folder.trug.json` first, knows every file and its role, and can navigate directly to what it needs.

---

## The Pipeline

```
WEB_HUB (research) → AAA (plan) → EPIC (track) → TRUG (graph) → TRL (specify) → Document (deliver) → MEMORY (remember) → FOLDER (index)
```

Every system feeds the next. The output is a signable NDA. The infrastructure is a machine-readable graph that any LLM can navigate, verify, and build on.

## Jurisdiction

Washington State — RCW 19.108 (Uniform Trade Secrets Act), King County.
