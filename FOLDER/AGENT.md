# FOLDER — Agent Instructions

<trl>
DEFINE "folder.trug.json" AS DATA graph 'for MODULE folder.
EACH MODULE folder SHALL CONTAIN EXACTLY A FILE folder.trug.json.
FILE folder.trug.json SHALL 'be RECORD ground_truth 'for MODULE folder.
AGENT SHALL READ FILE folder.trug.json 'at ENTRY MODULE folder.
AGENT SHALL UPDATE FILE folder.trug.json WHEN AGENT MODIFY MODULE folder.
</trl>

A `folder.trug.json` is a TRUG graph that indexes a directory. Every file is a node. Every relationship is an edge. You read it to know what exists, what each file does, and how things connect — without opening every file.

---

## The Four-File Pattern

<trl>
EACH MODULE folder MAY CONTAIN FILE folder.trug.json AND FILE README.md AND FILE ARCHITECTURE.md AND FILE AAA.md.
FILE folder.trug.json SHALL 'be RECORD ground_truth.
FILE README.md SHALL 'be RECORD narrative 'for PARTY human.
FILE ARCHITECTURE.md SHALL 'be RECORD auto_generated FROM FILE folder.trug.json.
FILE AAA.md SHALL 'be RECORD auto_generated FROM ENDPOINT github_issue.
NO AGENT SHALL MODIFY FILE ARCHITECTURE.md.
NO AGENT SHALL MODIFY FILE AAA.md.
</trl>

| File | Owner | Agent Action |
|------|-------|-------------|
| **folder.trug.json** | Human-maintained | Read first. Update when files change. |
| **README.md** | Human-written | Read for motivation if needed. |
| **ARCHITECTURE.md** | Auto-generated nightly | Never edit. Read for rendered reference. |
| **AAA.md** | Auto-generated from GitHub Issues | Never edit. Read for active work spec. |

### How to Enter a Folder

<trl>
AGENT SHALL READ FILE folder.trug.json THEN READ FILE AAA.md IF EXISTS THEN READ FILE README.md IF REQUIRED.
AGENT SHALL SKIP FILE ARCHITECTURE.md — DATA 'is 'in FILE folder.trug.json.
AGENT SHALL SKIP ALL FILE 'with PREFIX "zzz_" — RECORD archived.
</trl>

1. Read `folder.trug.json` — know every file, component, and relationship
2. Read `AAA.md` (if present) — know the current task and phase
3. Read `README.md` only if you need motivation or context
4. Skip `ARCHITECTURE.md` — same data as the TRUG, just rendered
5. Skip `zzz_*` files — archived, irrelevant

---

## Node Types

<trl>
DEFINE "FOLDER" AS DATA node 'at KILO METRIC_LEVEL — THE FOLDER ITSELF.
DEFINE "DOCUMENT" AS DATA node 'at BASE METRIC_LEVEL — MARKDOWN FILE.
DEFINE "SPECIFICATION" AS DATA node 'at BASE METRIC_LEVEL — SPEC OR PROTOCOL FILE.
DEFINE "COMPONENT" AS DATA node 'at DEKA METRIC_LEVEL — MAJOR CODE SUBSYSTEM.
DEFINE "TEST_SUITE" AS DATA node 'at BASE METRIC_LEVEL — TEST DIRECTORY OR COLLECTION.
DEFINE "EXAMPLE_SET" AS DATA node 'at BASE METRIC_LEVEL — EXAMPLES DIRECTORY.
DEFINE "SCHEMA" AS DATA node 'at BASE METRIC_LEVEL — JSON SCHEMA FILE.
DEFINE "TEMPLATE" AS DATA node 'at BASE METRIC_LEVEL — GENERATOR TEMPLATE.
EACH DATA node SHALL CONTAIN RECORD id AND RECORD type AND RECORD properties AND RECORD parent_id AND RECORD contains AND RECORD metric_level AND RECORD dimension.
</trl>

| Type | What It Represents | metric_level |
|------|-------------------|-------------|
| `FOLDER` | The folder itself — exactly one, root node | `KILO_FOLDER` |
| `DOCUMENT` | Markdown docs (README, guides, references) | `BASE_DOCUMENT` |
| `SPECIFICATION` | Spec and protocol files — define behavior | `BASE_SPECIFICATION` |
| `COMPONENT` | A major code subsystem (validator, CLI, engine) | `DEKA_COMPONENT` |
| `TEST_SUITE` | A test directory or collection | `BASE_TEST_SUITE` |
| `EXAMPLE_SET` | An examples directory or collection | `BASE_EXAMPLE_SET` |
| `SCHEMA` | A JSON Schema file | `BASE_SCHEMA` |
| `TEMPLATE` | A generator template | `BASE_TEMPLATE` |

### Node Properties

<trl>
EACH DATA node SHALL CONTAIN RECORD name 'in RECORD properties.
EACH DATA node SHALL CONTAIN RECORD purpose 'in RECORD properties — A RECORD sentence DESCRIBING WHAT FILE DOES.
DATA node MAY CONTAIN RECORD format AND RECORD status AND RECORD stale AND RECORD verified.
IF RECORD stale EQUALS TRUE THEN FILE 'is MISSING FROM DISK.
IF RECORD planned EQUALS TRUE THEN FILE 'will 'be CREATED BY FUTURE RECORD issue.
IF RECORD verified EQUALS TRUE THEN PARTY human 'has CONFIRMED DATA node 'is ACCURATE.
</trl>

Every node has a `purpose` field — one sentence explaining what the file does. This is what saves tokens: you read the purpose instead of opening the file.

```json
{
  "id": "doc_specification",
  "type": "SPECIFICATION",
  "properties": {
    "name": "SPEC_computation.md",
    "purpose": "Formal specification for TRUGS Computation — 23-operation vocabulary, type system, and 6 validation rules",
    "format": "markdown"
  },
  "parent_id": "computation_folder",
  "contains": [],
  "metric_level": "BASE_SPECIFICATION",
  "dimension": "folder_structure"
}
```

---

## Edge Relations

<trl>
DEFINE "contains" AS DATA edge — FOLDER DIRECTLY CONTAINS THIS NODE.
DEFINE "uses" AS DATA edge — RUNTIME OR BUILD DEPENDENCY.
DEFINE "produces" AS DATA edge — THIS COMPONENT GENERATES 'that OUTPUT.
DEFINE "validates" AS DATA edge — THIS NODE VALIDATES 'that NODE.
DEFINE "implements" AS DATA edge — CODE 'that REALIZES A SPEC.
DEFINE "tests" AS DATA edge — TEST SUITE COVERS THIS COMPONENT.
DEFINE "describes" AS DATA edge — DOCUMENT EXPLAINS THIS NODE.
DEFINE "governs" AS DATA edge — OWNS POLICY OR COMPLIANCE RULES.
EACH DATA edge SHALL CONTAIN RECORD from_id AND RECORD to_id AND RECORD relation AND RECORD properties.
RECORD properties SHALL 'be OBJECT — MUST 'be PRESENT EVEN WHEN EMPTY.
</trl>

| Relation | From → To | Meaning |
|----------|-----------|---------|
| `contains` | FOLDER → any | Folder directly contains this node |
| `uses` | any → COMPONENT, SPEC, SCHEMA | Runtime or build-time dependency |
| `produces` | COMPONENT, TEMPLATE → DOCUMENT, EXAMPLE_SET | This component generates that output |
| `validates` | SCHEMA, COMPONENT → any | This node validates that node |
| `implements` | COMPONENT → SPECIFICATION | Code that realizes a spec |
| `tests` | TEST_SUITE → COMPONENT | Test suite covers this component |
| `describes` | DOCUMENT → any | Document explains this node |
| `governs` | FOLDER, SPECIFICATION → any | Owns policy or compliance rules |

### Edge Format

```json
{
  "from_id": "validator_component",
  "to_id": "spec_validation",
  "relation": "implements",
  "properties": {}
}
```

### Cross-Folder Edges

<trl>
DATA edge MAY REFERENCE DATA node 'in ANOTHER MODULE folder.
CROSS-FOLDER RECORD to_id SHALL USE RECORD syntax "folder_name:node_id".
EACH MODULE folder SHALL DECLARE ONLY ITS OWN OUTBOUND DATA edge.
NO MODULE folder SHALL DECLARE DATA edge 'for ANOTHER MODULE folder.
</trl>

When a node depends on something in another folder, use qualified IDs:

```json
{
  "from_id": "validator_component",
  "to_id": "trugs_protocol:spec_validation",
  "relation": "implements",
  "properties": {}
}
```

The prefix before `:` is the folder name. Each folder declares its own outbound edges. No folder speaks for another.

---

## Building a folder.trug.json

<trl>
AGENT SHALL BUILD FILE folder.trug.json FROM RECORD filesystem — NOT FROM FILE AAA.md OR FILE README.md.
AGENT SHALL COUNT FILE 'on DISK USING RECORD command ls OR find OR wc.
AGENT SHALL READ RECORD source — FILE pyproject.toml AND RECORD test_runner AND RECORD directory_listing.
AGENT SHALL VERIFY EACH RECORD numeric_property AGAINST RECORD filesystem 'before COMMIT.
NO AGENT SHALL USE RECORD prose_document AS SOURCE 'for RECORD count OR RECORD file_list.
</trl>

### The Hard Rule

**The filesystem is the source of truth.** Not AAA.md. Not README.md. Not prose documents. Count files on disk. Read actual source. Verify every number.

| Data Needed | Source | NOT This |
|-------------|--------|----------|
| File counts | `ls`, `find`, `wc -l` | AAA.md prose |
| Component list | Directory listing + imports | AAA.md component section |
| Test count | Test runner output | AAA.md status line |
| Schema list | `ls schemas/*.json` | AAA.md table |
| Phase/status | AAA.md (this IS intent data) | — |
| Edge relationships | Code inspection + human judgment | — |

### Step by Step

<trl>
AGENT SHALL LIST ALL FILE 'in MODULE folder.
'for EACH FILE AGENT SHALL CREATE DATA node 'with RECORD type AND RECORD purpose.
AGENT SHALL CREATE EXACTLY A DATA node 'of TYPE FOLDER AS RECORD root.
AGENT SHALL SET RECORD parent_id AND RECORD contains 'for HIERARCHY.
AGENT SHALL CREATE DATA edge 'for EACH RECORD relationship 'between DATA node.
AGENT SHALL VALIDATE FILE folder.trug.json.
</trl>

1. **List files on disk** — `ls`, `find`
2. **Create the FOLDER node** — one root node, `parent_id: null`
3. **Create a node for each file/component** — type it correctly, write a one-sentence purpose
4. **Set hierarchy** — `parent_id` points up, `contains` points down, both must agree
5. **Create edges** — `implements`, `tests`, `uses`, `describes`, etc.
6. **Validate** — run `trugs-folder-check` or `python tools/validate.py`

---

## Lifecycle Properties

<trl>
IF FILE 'is MISSING FROM DISK THEN AGENT SHALL SET RECORD stale TO TRUE 'on DATA node.
IF FILE 'will 'be CREATED BY FUTURE RECORD issue THEN PARTY human SHALL SET RECORD planned TO TRUE.
IF PARTY human CONFIRMS DATA node 'is ACCURATE THEN PARTY human SHALL SET RECORD verified TO TRUE.
IF FILE folder.trug.json CHANGES AFTER RECORD verified 'is SET THEN RECORD verified SHALL 'be CLEARED.
</trl>

| Property | Set By | Meaning |
|----------|--------|---------|
| `stale: true` | Automation | File was here, now gone from disk |
| `stale_reason` | Automation | Why the node is stale |
| `planned: true` | Human | File will be created by a future issue |
| `planned_issue` | Human | GitHub issue that will create the file |
| `verified: true` | Human | Human confirmed this node is accurate |
| `verified_by` | Human | Who verified it |
| `verified_date` | Human | When it was verified |

### Trust Signal

| verified | stale | Interpretation |
|----------|-------|---------------|
| true | false | Fully trusted — human confirmed, unchanged since |
| false | false | Unreviewed — synced but no human sign-off |
| false | true | Stale — drift detected, downgrade trust |
| true | true | Conflict — human verified but drift detected since |

---

## Maintaining folder.trug.json

<trl>
IF AGENT CREATE FILE 'in MODULE folder THEN AGENT SHALL ADD DATA node TO FILE folder.trug.json.
IF AGENT DELETE FILE 'in MODULE folder THEN AGENT SHALL SET RECORD stale TO TRUE 'on DATA node.
IF AGENT CREATE RECORD relationship THEN AGENT SHALL ADD DATA edge.
AGENT SHALL_NOT REMOVE DATA node — SET RECORD stale INSTEAD.
AGENT SHALL UPDATE RECORD purpose IF FILE RECORD content CHANGES SIGNIFICANTLY.
</trl>

- **New file** → add a node with type and purpose
- **Deleted file** → set `stale: true` on the node (never remove nodes)
- **New relationship** → add an edge
- **Changed file** → update the purpose if the file's role changed
- **Renamed file** → update the `name` property, keep the same `id`

---

## Document Naming Convention

<trl>
EACH FILE CREATED BY PARTY human SHALL FOLLOW RECORD pattern "TYPE_description.md".
RECORD TYPE SHALL 'be UPPERCASE — TELLS RECORD type WITHOUT READING FILE.
RECORD description SHALL 'be LOWERCASE 'with UNDERSCORES.
</trl>

```
TYPE_description_in_lowercase.md
```

Valid types: `VISION`, `SPEC`, `PROPOSAL`, `RESEARCH`, `GUIDE`, `PLAN`, `REPORT`, `ANALYSIS`, `REFERENCE`, `PITCH`, `PROMPT`, `AUDIT`, `STANDARD`, `MIGRATION`, `ROADMAP`, `TODO`

An agent seeing `SPEC_computation.md` knows it's a specification about computation — without opening the file. Compare with `notes.md` or `design.md` where you'd have to read it to find out.

---

## The zzz_ Archive Convention

<trl>
NO AGENT SHALL READ FILE 'with PREFIX "zzz_".
NO AGENT SHALL REFERENCE FILE 'with PREFIX "zzz_" 'in DATA graph.
NO AGENT SHALL CREATE DATA node 'for FILE 'with PREFIX "zzz_".
FILE 'with PREFIX "zzz_" 'is RECORD archived — INVISIBLE TO AGENT.
</trl>

Files prefixed with `zzz_` are archived — pending human review before deletion. They sort to the bottom of directory listings. They are invisible to agents and to the graph. Never read, reference, or index them.

---

## CLI Tools

<trl>
AGENT MAY USE RECORD command "trugs-folder-init" TO CREATE FILE folder.trug.json FROM RECORD filesystem.
AGENT MAY USE RECORD command "trugs-folder-sync" TO UPDATE FILE folder.trug.json FROM RECORD filesystem.
AGENT SHALL USE RECORD command "trugs-folder-check" TO VALIDATE FILE folder.trug.json.
AGENT MAY USE RECORD command "trugs-folder-render" TO GENERATE FILE ARCHITECTURE.md FROM FILE folder.trug.json.
</trl>

```bash
trugs-folder-init [PATH]              # Generate starter folder.trug.json from directory scan
trugs-folder-sync [PATH] [--all]      # Add nodes for new files, mark missing files stale
trugs-folder-check [PATH] [--all]     # Validate folder.trug.json — exit 0 = pass, exit 1 = errors
trugs-folder-render [PATH] [--all]    # Regenerate ARCHITECTURE.md from folder.trug.json
```

`trugs-folder-sync` rules:
- Adds nodes for new files found on disk
- Sets `stale: true` on nodes whose files are missing
- Never removes nodes
- Never modifies human-curated edges

See [EXAMPLE_folder.trug.json](EXAMPLE_folder.trug.json) for a complete example.
