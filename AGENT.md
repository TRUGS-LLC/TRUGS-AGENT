# TRUGS Agent System

<trl>
DEFINE "TRUGS" AS NAMESPACE.
DEFINE "TRL" AS INTERFACE.
NAMESPACE TRUGS GOVERNS ALL DATA graph AND ALL RECORD sentence.
INTERFACE TRL GOVERNS ALL RECORD sentence.
AGENT SHALL READ THIS FILE THEN IMPLEMENT ALL RECORD instruction.
</trl>

You are an agent that speaks TRL. This file teaches the language. Component folders teach the methodology.

| Component | What it teaches | File |
|-----------|----------------|------|
| **Folder** | Machine-readable filesystem index | `FOLDER/AGENT.md` |
| **AAA** | 9-phase development protocol | `AAA/AGENT.md` |
| **EPIC** | Portfolio tracking as a graph | `EPIC/AGENT.md` |
| **Memory** | Persistent context across sessions | `MEMORY/AGENT.md` |
| **Trugging** | Describing a codebase with TRUGs and TRL | `TRUGGING/AGENT.md` |
| **Web Hub** | Curated web resource landscape | `WEB_HUB/AGENT.md` |
| **Skills** | Composable agent actions — primitives and compounds | `SKILLS/AGENT.md` |

Read this file first. Read component files when you need that component.

---

## TRL vs TRUGS — When to Use Which

<trl>
DEFINE "TRL" AS INTERFACE 'for RECORD sentence.
DEFINE "TRUGS" AS INTERFACE 'for DATA graph.
EACH RECORD sentence SHALL COMPILE TO DATA graph.
EACH DATA graph SHALL COMPILE TO RECORD sentence.
</trl>

**TRL (sentences)** — use when communicating. Instructions, specifications, acceptance criteria, code comments. Human writes it, agent reads it, both understand it.

**TRUGS (graphs)** — use when storing and executing. Project tracking, validation, traversal, state management. Machines read it, tools validate it, agents navigate it.

| Situation | Use | Why |
|-----------|-----|-----|
| Writing instructions | TRL | Human-readable, agent-executable |
| Code comments | TRL | Compilable documentation |
| Acceptance criteria | TRL | Both human and agent verify against it |
| Project tracking | TRUGS | Machines traverse and validate |
| Development phases | TRL | Communication between human and agent |
| Execution state | TRUGS | Agent tracks progress as graph nodes |
| Memory files | English + TRL | Context for future sessions |
| Validation rules | TRUGS | Tools enforce mechanically |

The sentence is the graph. The graph is the sentence. TRL is how you talk about it. TRUGS is how you store it.

### Side-by-Side Example

**TRL (the sentence):**

```
<trl>
SERVICE api SHALL AUTHENTICATE PARTY user
  THEN READ DATA FROM STREAM database
  THEN WRITE RESULT TO PARTY user
  OR THROW EXCEPTION.
IF SERVICE api THROW EXCEPTION
  THEN SERVICE api SHALL SEND ERROR TO PARTY user.
</trl>
```

**TRUGS (the graph):**

```json
{
  "nodes": [
    {"id": "api", "type": "SERVICE", "properties": {"name": "api"}, "parent_id": null, "contains": [], "metric_level": "BASE_SERVICE", "dimension": "system"},
    {"id": "user", "type": "PARTY", "properties": {"name": "user"}, "parent_id": null, "contains": [], "metric_level": "BASE_PARTY", "dimension": "system"},
    {"id": "database", "type": "STREAM", "properties": {"name": "database"}, "parent_id": null, "contains": [], "metric_level": "BASE_STREAM", "dimension": "system"},
    {"id": "op_auth", "type": "FUNCTION", "properties": {"operation": "AUTHENTICATE", "modal": "SHALL"}, "parent_id": "api", "contains": [], "metric_level": "CENTI_FUNCTION", "dimension": "system"},
    {"id": "op_read", "type": "FUNCTION", "properties": {"operation": "READ"}, "parent_id": "api", "contains": [], "metric_level": "CENTI_FUNCTION", "dimension": "system"},
    {"id": "op_write", "type": "FUNCTION", "properties": {"operation": "WRITE"}, "parent_id": "api", "contains": [], "metric_level": "CENTI_FUNCTION", "dimension": "system"},
    {"id": "op_throw", "type": "EXCEPTION", "properties": {"operation": "THROW"}, "parent_id": "api", "contains": [], "metric_level": "CENTI_EXCEPTION", "dimension": "system"},
    {"id": "op_send_error", "type": "FUNCTION", "properties": {"operation": "SEND", "object": "ERROR"}, "parent_id": "api", "contains": [], "metric_level": "CENTI_FUNCTION", "dimension": "system"}
  ],
  "edges": [
    {"from_id": "op_auth", "to_id": "user", "relation": "AUTHENTICATE"},
    {"from_id": "op_auth", "to_id": "op_read", "relation": "THEN"},
    {"from_id": "op_read", "to_id": "database", "relation": "FROM"},
    {"from_id": "op_read", "to_id": "op_write", "relation": "THEN"},
    {"from_id": "op_write", "to_id": "user", "relation": "TO"},
    {"from_id": "op_write", "to_id": "op_throw", "relation": "OR"},
    {"from_id": "op_throw", "to_id": "op_send_error", "relation": "THEN"},
    {"from_id": "op_send_error", "to_id": "user", "relation": "TO"}
  ]
}
```

Same specification. Same structure. Different views.

---

## TRL — The Language

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
NO RECORD SHALL RECEIVE RECORD obligation UNLESS RECORD 'is PARTY.
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
NO RECORD sentence SHALL CONTAIN "NO" AND "SHALL_NOT" 'in SAME RECORD clause.
AGENT SHALL STRIP RECORD sugar 'before PARSE RECORD sentence.
</trl>

---

## Using TRL in Your Project

<trl>
PARTY human MAY WRITE RECORD trl_block 'in FILE code_comment OR FILE specification OR FILE issue OR FILE config.
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
SERVICE api SHALL AUTHENTICATE ALL PARTY 'before READ DATA.
NO SERVICE api SHALL WRITE INVALID RECORD TO STREAM database.
SERVICE api SHALL RETRY BOUNDED 3 WITHIN 30s OR THROW EXCEPTION.
</trl>
```

### In issue descriptions

```markdown
<trl>
AGENT SHALL CREATE MODULE email_mcp CONTAINS FUNCTION send AND FUNCTION read AND FUNCTION search.
EACH FUNCTION SHALL READ CONFIG FROM FILE accounts.json.
FUNCTION delete SHALL REQUIRE VALID CONFIRM 'before DELETE RECORD.
NO FUNCTION SHALL WRITE RECORD password TO FILE OR STREAM.
</trl>
```

---

## The Validator

TRUGS graphs are validated by `trugs-validate` — 16 rules that every graph must pass:

- **Rules 1-9 (structural)** — always enforced. Unique IDs, valid edge references, hierarchy consistency, required fields, correct types.
- **Rules 10-16 (compositional)** — enforced when graph declares `core_v1.0.0`. Subject-operation compatibility, modifier-entity compatibility, no double negation, reference scope.

```bash
python tools/validate.py my_graph.trug.json       # Validate one
python tools/validate.py --all my_project/         # Validate all
```

<trl>
AGENT SHALL VALIDATE ALL DATA graph SUBJECT_TO INTERFACE core_v1.0.0.
IF DATA graph 'is INVALID THEN AGENT SHALL FIX DATA graph THEN VALIDATE DATA graph.
NO AGENT SHALL DEPLOY INVALID DATA graph.
</trl>

---

## Quick Reference

<trl>
INTERFACE TRL CONTAINS 190 UNIQUE RECORD word.
EACH RECORD word SHALL 'have EXACTLY A RECORD meaning.
NO AGENT SHALL COMMIT TO BRANCH main.
NO AGENT SHALL MERGE RECORD pull_request.
</trl>

For component-specific instructions, read the AGENT.md in each folder:
- **FOLDER/AGENT.md** — filesystem indexing
- **AAA/AGENT.md** — development protocol
- **EPIC/AGENT.md** — portfolio tracking
- **MEMORY/AGENT.md** — persistent context
- **TRUGGING/AGENT.md** — codebase description
- **WEB_HUB/AGENT.md** — curated web resource landscape
- **SKILLS/AGENT.md** — composable agent actions (19 primitives, compound composition)

For the full TRL specification: https://github.com/TRUGS-LLC/TRUGS
