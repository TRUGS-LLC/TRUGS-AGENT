# NDA — Agent Instructions

<trl>
DEFINE "NDA" AS DATA graph FOR RECORD legal_agreement.
DEFINE "clause" AS DATA node IN DATA graph NDA.
EACH RECORD clause SHALL CONTAIN RECORD obligation OR RECORD prohibition OR RECORD definition.
AGENT SHALL READ THIS FILE THEN FOLLOW ALL RECORD step SEQUENTIAL.
</trl>

This folder demonstrates every TRUGS-AGENT system applied to drafting a mutual NDA under Washington State law. Follow these steps in order to understand how the systems connect.

---

## Step 1: Read the Research — WEB_HUB

<trl>
AGENT SHALL READ FILE web.trug.json FIRST.
AGENT SHALL IDENTIFY ALL RESOURCE node BY RECORD category — TEMPLATE AND GUIDE AND TOOL AND STANDARD.
AGENT SHALL FOLLOW DATA edge WITH HIGH RECORD weight TO FIND RECORD primary_sources.
AGENT SHALL USE RECORD purpose FIELD TO DECIDE RECORD relevance BEFORE FETCH RECORD url.
</trl>

**File:** `web.trug.json`
**System:** WEB_HUB
**What you learn:** 20 curated resources — NDA templates (Bonterms, uNDA), legal guidance (ABA, Contract Nerds), tools (Lumin, Spellbook), and statutes (RCW 19.108, DTSA, UTSA). Edges show how resources relate. Weights rank importance.

**How to use it:** When you need a citation, template language, or legal reference — traverse the web hub instead of searching the internet. Every resource has a `purpose` field so you know what it contains before fetching.

---

## Step 2: Read the Plan — AAA

<trl>
AGENT SHALL READ FILE AAA_nda_draft.md AFTER FILE web.trug.json.
AGENT SHALL IDENTIFY RECORD current_phase.
AGENT SHALL READ PHASE specifications FOR RECORD audit_criteria — THESE DEFINE "DONE".
AGENT SHALL READ PHASE architecture FOR RECORD coding_plan — THIS DEFINES RECORD execution_order.
AGENT SHALL_NOT DRAFT ANY RECORD clause UNLESS PHASE validation IS APPROVED.
</trl>

**File:** `AAA_nda_draft.md`
**System:** AAA
**What you learn:** The complete 9-phase plan. Phase 1 is the human's vision. Phases 2-4 are research, specs, and design. Phase 5 is human approval. Phases 6-8 are drafting, testing, and audit. Phase 9 is delivery.

**Critical sections:**
- **Phase 3 — SPECIFICATIONS:** defines 12 required clauses in TRL + 9 audit criteria
- **Phase 4 — ARCHITECTURE:** defines drafting order and design decisions (2yr term, 3yr survival, King County jurisdiction)
- **Phase 5 — VALIDATION:** human approved the plan before any drafting

**Key rule:** Phase 3 defines the audit. Phase 8 executes against it. The plan defines "done" before writing starts.

---

## Step 3: Read the Tracker — EPIC

<trl>
AGENT SHALL READ FILE epic.trug.json AFTER FILE AAA_nda_draft.md.
AGENT SHALL IDENTIFY ALL TASK WHERE RECORD status EQUALS "TODO" OR "IN_PROGRESS".
AGENT SHALL FOLLOW DATA edge OF RELATION BLOCKS TO UNDERSTAND RECORD execution_order.
AGENT SHALL_NOT START TASK IF BLOCKING TASK IS NOT DONE.
</trl>

**File:** `epic.trug.json`
**System:** EPIC
**What you learn:** 3 epics (Research, Draft, Review), 13 tasks, 11 BLOCKS dependency edges. The edges enforce drafting order — definitions before obligations, obligations before remedies, all clauses before audit, audit before human review.

**How to use it:** Read the BLOCKS edges to know what to work on next. The highest-priority TODO task with no blocking tasks is the next thing to do.

---

## Step 4: Read the NDA Graph — nda.trug.json

<trl>
AGENT SHALL READ FILE nda.trug.json AFTER FILE epic.trug.json.
AGENT SHALL IDENTIFY ALL DATA node OF TYPE RECORD — THESE ARE RECORD clause.
AGENT SHALL FOLLOW DATA edge OF RELATION DEPENDS_ON TO UNDERSTAND RECORD clause_dependencies.
AGENT SHALL FOLLOW DATA edge OF RELATION REFERENCES TO FIND RECORD bibliography_source.
AGENT SHALL USE RECORD properties ON EACH DATA node TO UNDERSTAND RECORD clause_requirements.
</trl>

**File:** `nda.trug.json`
**System:** FOLDER (applied to a legal document instead of a filesystem)
**What you learn:** The NDA's legal structure as a graph. 23 nodes: 12 clauses + 11 bibliography references. 26 edges: clause dependencies (DEPENDS_ON, GOVERNS) + source citations (REFERENCES).

**How to use it:**
- Traverse DEPENDS_ON edges to understand clause ordering — exclusions depend on definitions, remedies depend on obligations
- Traverse REFERENCES edges to find the legal source for each clause — Section 9 references RCW 19.108, Section 10 references DTSA § 1833(b)
- Read node `properties.purpose` for a one-sentence summary of each clause's role
- Read node `properties.defines` to see what terms each clause introduces

---

## Step 5: Read the TRL-Annotated NDA — EXAMPLE_nda_mutual.md

<trl>
AGENT SHALL READ FILE EXAMPLE_nda_mutual.md AFTER FILE nda.trug.json.
FOR EACH RECORD clause AGENT SHALL READ RECORD trl_block FIRST THEN RECORD plain_english.
RECORD trl_block IS RECORD formal_specification — THE OBLIGATION AS DEFINED.
RECORD plain_english IS RECORD human_readable — THE SAME OBLIGATION IN PROSE.
AGENT SHALL VERIFY RECORD plain_english MATCHES RECORD trl_block.
AGENT SHALL READ RECORD bibliography AT END FOR ALL RECORD source.
</trl>

**File:** `EXAMPLE_nda_mutual.md`
**System:** TRUGGING (TRL applied to legal text)
**What you learn:** Every clause written twice — TRL specification first, then plain English. The TRL is the formal contract. The English is the explanation.

**Example from Section 5:**

```
<trl>
PARTY receiving SHALL PROTECT RECORD confidential_info WITH REASONABLE RECORD measures.
PARTY receiving SHALL_NOT DISCLOSE RECORD confidential_info TO ANY PARTY
  EXCEPT RECORD authorized_representative WHO HAS RECORD obligation OF RECORD confidentiality.
</trl>

The Receiving Party shall:
(a) protect Confidential Information using at least the same degree of care...
```

**How to use it:**
- Verify the English matches the TRL — if they disagree, the TRL is authoritative
- Generate tests from the TRL — each SHALL/SHALL_NOT is a testable obligation
- The bibliography at the end maps every source to the sections it informed

---

## Step 6: Read the Clean Document — NDA_mutual_trugs_llc.md

<trl>
AGENT SHALL READ FILE NDA_mutual_trugs_llc.md AFTER FILE EXAMPLE_nda_mutual.md.
FILE NDA_mutual_trugs_llc.md IS RECORD final_output — NO RECORD trl_block AND NO RECORD annotation.
THIS FILE IS RECORD signable — READY FOR PARTY human TO SEND TO PARTY counterparty.
AGENT SHALL_NOT MODIFY THIS FILE WITHOUT FIRST MODIFYING FILE nda.trug.json AND FILE EXAMPLE_nda_mutual.md.
</trl>

**File:** `NDA_mutual_trugs_llc.md`
**System:** The output
**What you learn:** The finished NDA — plain English, 12 sections, no TRL, no graph references. This is what the counterparty receives.

**Key rule:** Changes flow through the pipeline. To change the clean document, first update `nda.trug.json` (the graph), then update `EXAMPLE_nda_mutual.md` (the TRL-annotated version), then regenerate `NDA_mutual_trugs_llc.md` (the clean output).

---

## Step 7: Read the Decisions — MEMORY

<trl>
AGENT SHALL READ FILE MEMORY.md AFTER ALL OTHER FILE.
AGENT SHALL USE RECORD memory TO UNDERSTAND RECORD decision AND RECORD preference.
IF AGENT DRAFT NEW RECORD agreement THEN AGENT SHALL APPLY RECORD memory — RECORD jurisdiction AND RECORD style AND RECORD term.
AGENT SHALL WRITE NEW RECORD memory IF NEW RECORD decision IS MADE.
</trl>

**File:** `MEMORY.md`
**System:** MEMORY
**What you learn:** Decisions and preferences from this project — WA state jurisdiction, 2-year term, plain English style, Bonterms as template baseline. If you draft another agreement, these carry forward.

---

## Step 8: Read the Index — folder.trug.json

<trl>
AGENT SHALL READ FILE folder.trug.json AT ENTRY MODULE NDA.
FILE folder.trug.json INDEXES ALL FILE IN MODULE NDA.
AGENT SHALL FOLLOW DATA edge OF RELATION "produces" TO UNDERSTAND RECORD pipeline.
DATA edge "produces" SHOWS: nda.trug.json PRODUCES EXAMPLE_nda_mutual.md PRODUCES NDA_mutual_trugs_llc.md.
</trl>

**File:** `folder.trug.json`
**System:** FOLDER
**What you learn:** All 10 files indexed with purpose descriptions and relationship edges. The `produces` edges show the pipeline: graph → TRL-annotated → clean document. The `governs` edges show what controls what: AAA governs the NDA graph, AGENT.md governs the folder.

**When entering this folder cold:** Read `folder.trug.json` first. It tells you what every file is and how they relate. Then follow the steps above in order.

---

## The Complete Pipeline

<trl>
STAGE research SHALL PRODUCE FILE web.trug.json.
STAGE plan SHALL READ FILE web.trug.json THEN PRODUCE FILE AAA_nda_draft.md.
STAGE track SHALL READ FILE AAA_nda_draft.md THEN PRODUCE FILE epic.trug.json.
STAGE graph SHALL READ FILE AAA_nda_draft.md THEN PRODUCE FILE nda.trug.json.
STAGE specify SHALL READ FILE nda.trug.json THEN PRODUCE FILE EXAMPLE_nda_mutual.md.
STAGE deliver SHALL READ FILE EXAMPLE_nda_mutual.md THEN PRODUCE FILE NDA_mutual_trugs_llc.md.
STAGE remember SHALL PRODUCE FILE MEMORY.md.
STAGE index SHALL PRODUCE FILE folder.trug.json.
EACH STAGE SHALL EXECUTE SEQUENTIAL.
</trl>

```
research → plan → track → graph → specify → deliver → remember → index
  (web)    (AAA)  (EPIC)  (TRUG)   (TRL)     (doc)    (memory)  (folder)
```

Every system feeds the next. The input is a human's vision. The output is a signable NDA. Everything in between is machine-readable infrastructure that any LLM can navigate, verify, and build on.
