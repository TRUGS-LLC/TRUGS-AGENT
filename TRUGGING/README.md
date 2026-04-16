# TRUGGING — How to Describe a Program with TRUGs and TRUG/L

Trugging is the methodology for describing a codebase at every level of granularity — from the whole system down to a single function. TRUGs (graphs) describe structure. TRUG/L (sentences) describe behavior. Together they give an LLM a complete, machine-readable picture of your program without reading every line of code.

## When to Use

Any codebase that an LLM will work on repeatedly. The upfront cost is small — a JSON file per major folder, a few sentences per file. The payoff is that your LLM stops guessing architecture and starts navigating it.

## Four Levels

### Level 1: System — `project.trug.json`

The whole program as a graph. Nodes are services, databases, external APIs, major modules. Edges are dependencies, data flows, ownership.

Your LLM reads this to answer: *what exists and what connects to what?*

### Level 2: Component — `folder.trug.json`

Each major folder gets its own graph. Nodes are files, classes, key interfaces. Edges are imports, implementations, calls.

Your LLM reads this to answer: *what's inside this module and how do the pieces fit together?*

### Level 3: File Header — `<trl>` block at top of file

A few TRUG/L sentences describing what the module does, what it must do, and what it must not do. Obligations, not implementation details.

Your LLM reads this to answer: *what are this module's contracts?*

### Level 4: Inline — `<trl>` in code comments

TRUG/L sentences on critical functions or blocks. Compilable contracts that an LLM can verify against the code, generate tests from, or detect drift on.

Your LLM reads this to answer: *what is this function's exact contract?*

## The Boundary Rule

Above the file boundary (system, folder): **use TRUGs**. You're mapping structure — things and relationships. Machines traverse it.

Inside the file boundary (header, inline): **use TRUG/L**. You're specifying behavior — actions and obligations. Humans read it, agents execute it.

**TRUGs are nouns. TRUG/L is verbs.**

## Example Walkthrough

An agent needs to fix a bug in the auth module:

1. Reads `project.trug.json` — finds `auth`, sees it connects to `api` and `db`
2. Reads `auth/folder.trug.json` — finds `handler.py`, `models.py`, sees `UserService` depends on `TokenValidator`
3. Reads `auth/handler.py` header TRUG/L — knows: must authenticate, must not log secrets, must handle expiration
4. Reads inline TRUG/L on `validate_token` — knows the function contract: validate JWT, throw on expired, return User

Four reads. System to function. No prose docs, no guessing, no asking the human.
