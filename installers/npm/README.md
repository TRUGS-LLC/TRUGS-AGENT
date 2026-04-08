# create-trugs-agent

A 190-word formal instruction language for LLM coding assistants. Your AI stops interpreting and starts executing.

## Usage

```bash
# Initialize for Claude Code (default)
npx create-trugs-agent

# Initialize for Cursor
npx create-trugs-agent cursor

# Initialize for GitHub Copilot
npx create-trugs-agent copilot
```

This copies AGENT.md (renamed for your IDE) and all component folders into the current directory. Your LLM reads the files and gains the TRL vocabulary — 190 words with exact definitions.

## What You Get

- **CLAUDE.md** (or `.cursorrules` / `.github/copilot-instructions.md`) — TRL vocabulary and grammar
- **AAA/** — 9-phase development protocol
- **EPIC/** — Portfolio tracking as a graph
- **FOLDER/** — Machine-readable filesystem index
- **MEMORY/** — Persistent context across sessions
- **SKILLS/** — 19 composable agent primitives
- **TRUGGING/** — Codebase description methodology
- **WEB_HUB/** — Curated web resource graph
- **tools/** — Zero-dependency TRUGS validator

## Links

- [GitHub](https://github.com/TRUGS-LLC/TRUGS-AGENT)
- [Full Specification](https://github.com/TRUGS-LLC/TRUGS)
- [Paper](https://github.com/TRUGS-LLC/TRUGS/blob/main/PAPER/trugs.pdf)

Apache 2.0 — TRUGS LLC
