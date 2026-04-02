# TRUGS Agent

**Copy files into your project. Your LLM reads them. You don't have to.**

## Install

Copy what you need into your project, renamed for your IDE:

| IDE | System prompt file |
|-----|-------------------|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Any other LLM | Paste contents as system prompt |

The root `AGENT.md` teaches TRL — the language everything else is built on. Each component folder has its own `AGENT.md` with complete instructions for that component. Copy the root plus whichever components you want.

## Components

| Folder | What It Does | Standalone? |
|--------|-------------|-------------|
| [FOLDER/](FOLDER/) | Machine-readable filesystem index — every file, component, and relationship in one JSON graph | Yes |
| [AAA/](AAA/) | 9-phase development protocol — plan before you code, audit before you ship | Yes |
| [EPIC/](EPIC/) | Portfolio tracker as a traversable graph — what's in progress, blocked, done | Yes |
| [MEMORY/](MEMORY/) | Persistent context across sessions — decisions, preferences, project state | Yes |
| [TRUGGING/](TRUGGING/) | Methodology for describing a codebase with TRUGs and TRL at every level | Yes |
| [WEB_HUB/](WEB_HUB/) | Curated web resource graph — papers, repos, tools, articles indexed as a TRUG | Yes |

Each folder contains:
- `README.md` — what the component is, when and why to use it (for you)
- `AGENT.md` — complete instructions for employing the component (for your LLM)
- Examples — real artifacts from production use

## Adopt One or All

Every component stands alone. You can use:
- **Just the root** — TRL vocabulary and grammar, formalized instructions in any project
- **Root + Folder** — filesystem indexing for any project
- **Root + AAA** — structured development without project tracking
- **Root + Memory** — persistent context without the full workflow
- **Root + Trugging** — codebase description without development process
- **Everything** — the complete system

## Tools

The `tools/` folder contains the TRUGS validator — 16 rules that enforce graph correctness. Zero dependencies, pure Python.

```bash
python tools/validate.py my_graph.trug.json          # Validate one
python tools/validate.py --all my_project/            # Validate all
```

## Why This Over Writing Good Prompts

English prompts are ambiguous. "Make sure the code is clean" means different things to different LLMs on different days.

TRL sentences have exactly one meaning. `AGENT SHALL VALIDATE ALL CODE BEFORE COMMIT` compiles to a graph with a specific obligation, a specific action, and a specific scope. The LLM doesn't interpret — it executes.

## Full Specification

- **TRL + TRUGS**: https://github.com/TRUGS-LLC/TRUGS
- **Paper**: https://github.com/TRUGS-LLC/TRUGS/blob/main/PAPER/trugs.pdf
- **DOI**: https://doi.org/10.5281/zenodo.19379454

## License

Apache 2.0 — TRUGS LLC
