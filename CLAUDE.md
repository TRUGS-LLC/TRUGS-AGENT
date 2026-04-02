# TRUGS Agent System

<trl>
DEFINE "TRUGS" AS NAMESPACE.
DEFINE "TRL" AS INTERFACE.
DEFINE "AAA" AS PIPELINE.
DEFINE "Memory" AS MODULE.

NAMESPACE TRUGS GOVERNS ALL DATA graph AND ALL RECORD sentence.
INTERFACE TRL GOVERNS ALL RECORD sentence.
PIPELINE AAA GOVERNS ALL PHASE.
MODULE Memory GOVERNS ALL RECORD memory.

AGENT SHALL READ THIS FILE THEN IMPLEMENT ALL RECORD instruction.
</trl>

You are an agent that speaks TRL, follows AAA, and maintains Memory. This file teaches you everything.

---

## TRL vs TRUGS — When to Use Which

<trl>
DEFINE "TRL" AS INTERFACE FOR RECORD sentence.
DEFINE "TRUGS" AS INTERFACE FOR DATA graph.
EACH RECORD sentence SHALL COMPILE TO DATA graph.
EACH DATA graph SHALL COMPILE TO RECORD sentence.
</trl>

**TRL (sentences)** — use when communicating. Instructions, specifications, acceptance criteria, code comments, issue descriptions. The human writes it, the agent reads it, both understand it.

**TRUGS (graphs)** — use when storing and executing. Project tracking, validation, traversal, state management. Machines read it, tools validate it, agents navigate it.

| Situation | Use | Why |
|-----------|-----|-----|
| Writing instructions | TRL | Human-readable, agent-executable |
| Code comments | TRL | Compilable documentation |
| Acceptance criteria | TRL | Both human and agent verify against it |
| Project tracking | TRUGS | Machines traverse and validate |
| AAA planning phases | TRL | Communication between human and agent |
| AAA execution state | TRUGS | Agent tracks progress as graph nodes |
| Memory files | English + TRL | Context for future sessions |
| Validation rules | TRUGS | Tools enforce mechanically |

The sentence is the graph. The graph is the sentence. TRL is how you talk about it. TRUGS is how you store it.

---

## Part 1: TRL — The Language

<trl>
DEFINE "TRL" AS INTERFACE.
INTERFACE TRL CONTAINS 190 UNIQUE RECORD word.
EACH RECORD word BELONGS_TO EXACTLY A RECORD part_of_speech.
EACH RECORD sentence SHALL COMPILE TO DATA graph.
EACH DATA graph SHALL COMPILE TO RECORD sentence.
</trl>

### Vocabulary (190 words)

**Nouns — things that exist (become graph nodes)**

<trl>
DEFINE "actor" AS PARTY OR AGENT OR PROCESS OR SERVICE OR FUNCTION OR TRANSFORM OR PRINCIPAL.
DEFINE "artifact" AS DATA OR FILE OR RECORD OR MESSAGE OR STREAM OR RESOURCE.
DEFINE "container" AS PIPELINE OR STAGE OR MODULE OR NAMESPACE.
DEFINE "boundary" AS ENTRY OR EXIT OR INTERFACE OR ENDPOINT.
DEFINE "outcome" AS ERROR OR EXCEPTION OR REMEDY.
</trl>

**Verbs — actions (become operation nodes)**

<trl>
DEFINE "transform" AS FILTER OR MAP OR SORT OR MERGE OR SPLIT OR AGGREGATE OR GROUP OR DISTINCT OR TAKE OR SKIP.
DEFINE "move" AS READ OR WRITE OR SEND OR RECEIVE OR REQUEST OR RESPOND OR AUTHENTICATE.
DEFINE "obligate" AS VALIDATE OR ASSERT OR REQUIRE.
DEFINE "permit" AS ALLOW OR APPROVE OR GRANT OR OVERRIDE.
DEFINE "prohibit" AS DENY OR REJECT OR REVOKE.
DEFINE "control" AS BRANCH OR MATCH OR RETRY OR TIMEOUT OR THROW OR EXISTS OR EXPIRE OR EQUALS OR EXCEEDS.
DEFINE "bind" AS DEFINE OR DECLARE OR IMPLEMENT OR NEST OR AUGMENT OR REPLACE OR CITE OR ADMINISTER.
DEFINE "resolve" AS CATCH OR HANDLE OR RECOVER.
</trl>

**Modals — obligation (modify verbs)**

<trl>
DEFINE "SHALL" AS REQUIRED RECORD obligation.
DEFINE "MAY" AS OPTIONAL RECORD permission.
DEFINE "SHALL_NOT" AS REQUIRED RECORD prohibition.
EACH RECORD obligation SHALL REQUIRE PARTY AS RECORD subject.
NO DATA SHALL RECEIVE RECORD obligation.
NO RECORD SHALL RECEIVE RECORD obligation UNLESS RECORD IS PARTY.
</trl>

- SHALL = MUST do this. Failure is a violation.
- MAY = ALLOWED but not required.
- SHALL_NOT = MUST NOT do this. Doing it is a violation.

**Adjectives — modify nouns (become node properties)**

<trl>
DEFINE "type" AS STRING OR INTEGER OR BOOLEAN OR ARRAY OR OBJECT.
DEFINE "access" AS PUBLIC OR PRIVATE OR CONFIDENTIAL OR READONLY.
DEFINE "state" AS VALID OR INVALID OR ACTIVE OR PENDING OR FAILED OR MUTABLE OR IMMUTABLE.
DEFINE "quantity" AS REQUIRED OR OPTIONAL OR UNIQUE OR MULTIPLE.
DEFINE "priority" AS CRITICAL OR HIGH OR LOW OR DEFAULT.
</trl>

**Adverbs — modify verbs (become operation properties)**

<trl>
DEFINE "timing" AS ASYNC OR SYNC OR PARALLEL OR SEQUENTIAL OR IMMEDIATE OR WITHIN.
DEFINE "repetition" AS ONCE OR ALWAYS OR NEVER OR BOUNDED.
DEFINE "degree" AS STRICTLY OR SUBSTANTIALLY OR REASONABLY.
</trl>

**Prepositions — relationships (become graph edges)**

<trl>
DEFINE "flow" AS FEEDS OR ROUTES OR TO OR FROM OR RETURNS_TO.
DEFINE "dependency" AS BINDS OR DEPENDS_ON OR IMPLEMENTS OR EXTENDS OR SUBJECT_TO.
DEFINE "authority" AS GOVERNS OR PURSUANT_TO OR ON_BEHALF_OF.
DEFINE "structure" AS CONTAINS OR REFERENCES OR SUPERSEDES.
DEFINE "binding" AS AS OR BY.
</trl>

**Conjunctions — connect clauses (become structural edges)**

<trl>
DEFINE "sequence" AS THEN OR FINALLY.
DEFINE "parallel" AS AND.
DEFINE "alternative" AS OR OR ELSE.
DEFINE "conditional" AS IF OR WHEN OR WHILE.
DEFINE "exception" AS UNLESS OR EXCEPT OR NOTWITHSTANDING OR PROVIDED_THAT OR WHEREAS.
</trl>

**Articles** — ALL, EACH, EVERY, ANY, SOME, A, THE, THIS, NO, NONE

**Pronouns** — SELF, RESULT, OUTPUT, INPUT, SOURCE, TARGET

**Sugar** — OF, IS, ARE, BE, BEEN, HAS, HAVE, WILL, THAT, WHICH, WHERE, WHO, INTO, UPON, WITH, FOR, AT, ON, PLEASE, ALSO, THEN_ALSO, THESE, THOSE, SUCH (compile to nothing — human readability only)

### How to Read and Execute

<trl>
AGENT SHALL STRIP ALL RECORD sugar FROM RECORD sentence.
AGENT SHALL PARSE RECORD sentence AS RECORD subject THEN RECORD modal THEN RECORD verb THEN RECORD object.
IF RECORD modal EQUALS "SHALL" THEN AGENT SHALL EXECUTE RECORD verb STRICTLY.
IF RECORD modal EQUALS "MAY" THEN AGENT MAY EXECUTE RECORD verb.
IF RECORD modal EQUALS "SHALL_NOT" THEN AGENT SHALL_NOT EXECUTE RECORD verb.
AGENT SHALL FOLLOW RECORD conjunction AS RECORD sequence.
</trl>

Parse example:
```
PARTY system SHALL FILTER ALL ACTIVE RECORD THEN WRITE RESULT TO ENDPOINT output.
```
- PARTY system → Actor node (subject)
- SHALL → obligation
- FILTER → Transform operation
- ALL ACTIVE RECORD → scoped, qualified artifact
- THEN → sequential conjunction
- WRITE RESULT TO ENDPOINT output → Move operation with destination

### Key Rules

<trl>
EACH RECORD word SHALL BELONG_TO EXACTLY A RECORD part_of_speech.
EACH RECORD modal SHALL REQUIRE PARTY AS RECORD subject.
EACH RECORD pronoun SHALL RESOLVE WITHIN THIS RECORD sentence.
NO RECORD sentence SHALL CONTAIN "NO" AND "SHALL_NOT" IN SAME RECORD clause.
AGENT SHALL STRIP RECORD sugar BEFORE PARSE RECORD sentence.
</trl>

---

## Part 2: AAA — Development Protocol

<trl>
DEFINE "AAA" AS PIPELINE CONTAINS PHASE vision AND PHASE feasibility AND PHASE specifications AND PHASE architecture AND PHASE validation AND PHASE coding AND PHASE testing AND PHASE audit AND PHASE deployment.
DEFINE "PLANNING" AS STAGE CONTAINS PHASE vision AND PHASE feasibility AND PHASE specifications AND PHASE architecture AND PHASE validation.
DEFINE "EXECUTION" AS STAGE CONTAINS PHASE coding AND PHASE testing AND PHASE audit AND PHASE deployment.
PIPELINE AAA CONTAINS STAGE PLANNING AND STAGE EXECUTION.
</trl>

### Two Paths — No Middle Ground

<trl>
IF AGENT KNOWS ALL REQUIRED STEP THEN AGENT SHALL EXECUTE AS RECORD chore.
IF AGENT REQUIRES RECORD specification OR RECORD decision THEN AGENT SHALL CREATE RECORD issue THEN EXECUTE PHASE vision.
NO AGENT SHALL CREATE RECORD issue FOR RECORD chore.
NO AGENT SHALL SKIP STAGE PLANNING FOR RECORD issue.
</trl>

| Path | Trigger | Flow |
|------|---------|------|
| **CHORE** | You know exactly what to do | Branch → do it → PR → human merges |
| **ISSUE** | Something is unknown | Issue → AAA → PLANNING → HITM → EXECUTION → PR → human merges |

When in doubt, start as a chore. If unknowns emerge, upgrade to an issue.

### PLANNING Cycle (phases 1-5)

<trl>
PARTY human SHALL DEFINE PHASE vision.
AGENT SHALL EXECUTE PHASE feasibility THEN PHASE specifications THEN PHASE architecture.
PHASE specifications SHALL CONTAIN RECORD audit_criteria.
PHASE architecture SHALL CONTAIN RECORD coding_plan.
PARTY human SHALL APPROVE PHASE validation.
NO AGENT SHALL EXECUTE STAGE EXECUTION UNLESS PARTY human APPROVE PHASE validation.
</trl>

| # | Phase | Who | Output |
|---|-------|-----|--------|
| 1 | **VISION** | Human | Problem + success criteria |
| 2 | **FEASIBILITY** | Agent | GO/NO-GO + risks |
| 3 | **SPECIFICATIONS** | Agent | Requirements + **audit criteria for Phase 8** |
| 4 | **ARCHITECTURE** | Agent | Design + ADRs + **coding plan** |
| 5 | **VALIDATION** | **Human approves** | Plan is complete → proceed to coding |

**Phase 3 defines the audit. Phase 8 executes against it.** The plan defines what "done" looks like before any code is written.

### VALIDATION Checks (Phase 5)

<trl>
AGENT SHALL VALIDATE PHASE specifications SUBJECT_TO PHASE vision.
AGENT SHALL VALIDATE PHASE architecture SUBJECT_TO PHASE specifications.
AGENT SHALL ASSERT PHASE specifications CONTAINS RECORD audit_criteria.
AGENT SHALL ASSERT PHASE architecture CONTAINS RECORD coding_plan.
AGENT SHALL ASSERT RECORD audit_criteria REFERENCES PHASE specifications.
NO AGENT SHALL PROCEED UNLESS ALL VALIDATION IS VALID.
</trl>

### EXECUTION Cycle (phases 6-9)

<trl>
AGENT SHALL EXECUTE PHASE coding SUBJECT_TO RECORD coding_plan.
AGENT SHALL EXECUTE PHASE testing THEN PHASE audit.
PHASE audit SHALL VALIDATE RESULT SUBJECT_TO RECORD audit_criteria FROM PHASE specifications.
IF PHASE audit IS INVALID THEN AGENT SHALL FIX CODE THEN EXECUTE PHASE testing THEN EXECUTE PHASE audit.
EACH PHASE audit ROUND SHALL FIX ALL RECORD finding AND WRITE RECORD test FOR EACH RECORD finding.
NO AGENT SHALL EXECUTE PHASE deployment UNLESS PHASE audit IS VALID.
PARTY human SHALL APPROVE PHASE deployment.
</trl>

| # | Phase | Who | Output |
|---|-------|-----|--------|
| 6 | **CODING** | Agent | Working code per coding plan |
| 7 | **TESTING** | Agent | All tests pass |
| 8 | **AUDIT** | Agent + **Human approves** | Check against Phase 3 criteria. Cycles until clean. |
| 9 | **DEPLOYMENT** | Agent creates PR. **Human merges.** | Shipped |

### Hard Rules

<trl>
NO AGENT SHALL COMMIT TO BRANCH main.
NO AGENT SHALL MERGE RECORD pull_request.
AGENT SHALL CREATE BRANCH THEN CREATE RECORD pull_request THEN STOP.
PARTY human SHALL MERGE RECORD pull_request.
NO AGENT SHALL EXECUTE PHASE coding UNLESS PHASE validation IS VALID.
NO AGENT SHALL EXECUTE PHASE deployment UNLESS PHASE audit IS VALID.
</trl>

---

## Part 3: Memory — Persistent Context

<trl>
DEFINE "Memory" AS MODULE CONTAINS RECORD user AND RECORD feedback AND RECORD project AND RECORD reference.
AGENT SHALL READ FILE MEMORY.md AT ENTRY session.
AGENT SHALL WRITE RECORD decision TO MODULE Memory DURING RECORD session.
AGENT SHALL WRITE RECORD summary TO MODULE Memory AT EXIT session.
</trl>

### Memory Types

<trl>
DEFINE "user" AS RECORD FOR PARTY human CONTAINS RECORD role AND RECORD preference AND RECORD expertise.
DEFINE "feedback" AS RECORD FOR RECORD correction OR RECORD confirmation.
DEFINE "project" AS RECORD FOR RECORD decision OR RECORD status OR RECORD deadline.
DEFINE "reference" AS RECORD FOR ENDPOINT external_system.
</trl>

| Type | Save when | Example |
|------|----------|---------|
| **user** | You learn about their role or preferences | "User is a data scientist focused on observability" |
| **feedback** | They correct you OR confirm a non-obvious approach | "Don't mock the database — use real DB in tests" |
| **project** | You learn who does what, why, or by when | "Merge freeze 2026-03-05 for mobile release" |
| **reference** | You learn about external resources | "Pipeline bugs tracked in Linear project INGEST" |

### What NOT to Save

<trl>
NO AGENT SHALL WRITE RECORD memory FOR DATA code_pattern.
NO AGENT SHALL WRITE RECORD memory FOR DATA git_history.
NO AGENT SHALL WRITE RECORD memory FOR DATA THAT EXISTS IN FILE CLAUDE.md.
NO AGENT SHALL WRITE RECORD memory FOR RECORD ephemeral_task.
</trl>

### Memory File Format

```markdown
---
name: short title
description: one-line description
type: user|feedback|project|reference
---

Content here.

**Why:** reason for the decision
**How to apply:** when this should influence future work
```

### MEMORY.md Index

<trl>
EACH RECORD memory SHALL REFERENCE FILE memory_file.md.
FILE MEMORY.md SHALL CONTAIN A RECORD pointer FOR EACH RECORD memory.
EACH RECORD pointer SHALL BE LESS_THAN 150 STRING characters.
</trl>

```markdown
# Memory Index
- [user_role.md](user_role.md) — Senior backend engineer, new to React
- [feedback_no_mocks.md](feedback_no_mocks.md) — Integration tests hit real DB, not mocks
```

### Session Pattern

<trl>
AGENT SHALL READ FILE MEMORY.md AT ENTRY session.
AGENT SHALL WRITE RECORD decision TO MODULE Memory WHEN RECORD decision EXISTS.
AGENT SHALL WRITE RECORD session_summary AT EXIT session.
AGENT SHALL WRITE RECORD pointer TO FILE MEMORY.md FOR EACH NEW RECORD memory.
</trl>

---

## Part 4: Using TRL in Your Project

<trl>
PARTY human MAY WRITE RECORD trl_block IN FILE code_comment OR FILE specification OR FILE issue OR FILE config.
AGENT SHALL READ RECORD trl_block THEN COMPILE TO DATA graph THEN EXECUTE.
</trl>

### In code comments

```python
# <trl>FUNCTION validate SHALL VALIDATE ALL REQUIRED RECORD
#   SUBJECT_TO INTERFACE schema.
# IF FUNCTION validate THROW EXCEPTION
#   THEN SEND ERROR TO PARTY caller.</trl>
def validate(records, schema):
    for record in records:
        if not schema.validate(record):
            raise ValidationError(record.id)
```

### In specifications

```markdown
<trl>
SERVICE api SHALL RESPOND WITHIN 200ms.
SERVICE api SHALL AUTHENTICATE ALL PARTY BEFORE READ DATA.
NO SERVICE api SHALL WRITE INVALID RECORD TO STREAM database.
SERVICE api SHALL RETRY BOUNDED 3 WITHIN 30s OR THROW EXCEPTION.
</trl>
```

### In issue descriptions

```markdown
<trl>
AGENT SHALL CREATE MODULE email_mcp CONTAINS FUNCTION send AND FUNCTION read AND FUNCTION search.
EACH FUNCTION SHALL READ CONFIG FROM FILE accounts.json.
FUNCTION delete SHALL REQUIRE VALID CONFIRM BEFORE DELETE RECORD.
NO FUNCTION SHALL WRITE RECORD password TO FILE OR STREAM.
</trl>
```

---

## Quick Reference

<trl>
INTERFACE TRL CONTAINS 190 UNIQUE RECORD word.
EACH RECORD word SHALL HAVE EXACTLY A RECORD meaning.
PIPELINE AAA CONTAINS 9 PHASE AND 2 STAGE AND 3 RECORD touchpoint.
PHASE specifications SHALL DEFINE RECORD audit_criteria.
PHASE audit SHALL EXECUTE SUBJECT_TO RECORD audit_criteria.
NO AGENT SHALL COMMIT TO BRANCH main.
NO AGENT SHALL MERGE RECORD pull_request.
MODULE Memory SHALL PERSIST RECORD context ACROSS RECORD session.
</trl>

For the full TRL specification: https://github.com/TRUGS-LLC/TRUGS
