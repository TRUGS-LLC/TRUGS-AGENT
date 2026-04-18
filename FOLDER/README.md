# FOLDER — Machine-Readable Filesystem Index

A `folder.trug.json` is a TRUG graph that indexes the contents of a directory — every file, every component, every relationship — so your LLM can navigate a codebase without reading everything in it.

## When to Use

Any project folder that an LLM will work in repeatedly. The cost is one JSON file per folder. The payoff is that your LLM stops wasting tokens reading files just to figure out what they are.

## The Problem It Solves

LLMs read everything in their context window. Every file costs tokens. Every irrelevant file wastes capacity. Every ambiguously named file forces the agent to open it just to decide if it matters.

The solution is not fewer files — it's a machine-readable index. One JSON file tells the agent what exists, what each file does, and how things relate. The agent reads the index, picks what it needs, and skips everything else.

## The Four-File Pattern

Every folder that matters has up to four standard files:

| File | Who Writes It | What It Does |
|------|--------------|--------------|
| **folder.trug.json** | Human (maintained) | Machine-readable graph — ground truth of contents and relationships |
| **README.md** | Human | Prose quickstart — motivation, purpose, getting started |
| **ARCHITECTURE.md** | Auto-generated | Dense technical reference rendered from folder.trug.json |
| **AAA.md** | Auto-generated | Active work spec rendered from GitHub Issues |

An agent entering any folder reads `folder.trug.json` first. Two to three files and it has full context.

## How It Works

A `folder.trug.json` is a TRUG graph where:
- **Nodes** are files, components, specs, test suites, schemas — anything in the folder
- **Edges** are relationships: `implements`, `tests`, `uses`, `describes`, `governs`
- **Hierarchy** shows what belongs to what via `parent_id` and `contains`

Each node has a `purpose` field — one sentence explaining what the file does. An agent reads this instead of opening the file.

## Node Types

| Type | Represents |
|------|-----------|
| `FOLDER` | The folder itself (exactly one, root node) |
| `DOCUMENT` | Markdown docs (README, guides, references) |
| `SPECIFICATION` | Spec and protocol files |
| `COMPONENT` | A major code subsystem |
| `TEST_SUITE` | A test directory or collection |
| `EXAMPLE_SET` | An examples directory or collection |
| `SCHEMA` | A JSON Schema file |
| `TEMPLATE` | A generator template |

## Edge Relations

| Relation | Meaning |
|----------|---------|
| `contains` | Folder directly contains this node |
| `uses` | Runtime or build-time dependency |
| `produces` | This component generates that output |
| `validates` | This node validates that node |
| `implements` | Code that realizes a spec |
| `tests` | Test suite covers this component |
| `describes` | Document explains this node |
| `governs` | Owns policy or compliance rules |

## CLI Tools

```bash
tg init [PATH]    # Generate starter folder.trug.json from directory scan
tg sync [PATH]    # Update nodes for new/missing files
tg check [PATH]   # Validate folder.trug.json — exit 0 = pass
tg render [PATH]  # Regenerate ARCHITECTURE.md from folder.trug.json
```

## Example

See [EXAMPLE_folder.trug.json](EXAMPLE_folder.trug.json) for a real folder.trug.json from a Python module with specs, components, tests, and cross-folder edges.
