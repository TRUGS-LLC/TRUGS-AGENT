# TRUGS Agent

**This repo is installed by copying one file into your project. Your LLM reads it. You don't have to.**

## Install

1. Copy `CLAUDE.md` to your project root
   - For Cursor: copy as `.cursorrules`
   - For GitHub Copilot: copy as `.github/copilot-instructions.md`
   - For any other LLM: paste the contents as your system prompt
2. Start a conversation with your LLM
3. It speaks TRL, runs AAA, remembers context

## What Your LLM Gets

**TRL** — A 190-word formalized English where every sentence compiles to a graph. Your LLM stops guessing what you mean because every word has exactly one meaning.

```
<trl>
AGENT SHALL CREATE BRANCH THEN WRITE CODE THEN RUN TEST.
IF TEST FAIL THEN AGENT SHALL FIX CODE THEN RUN TEST.
NO AGENT SHALL COMMIT TO BRANCH main.
</trl>
```

**AAA** — A 9-phase development protocol. Your LLM plans before it codes, defines audit criteria before it builds, and never ships without your approval.

**Memory** — Persistent context across sessions. Your LLM remembers decisions, preferences, and project state.

## Why This Over Writing Good Prompts

English prompts are ambiguous. "Make sure the code is clean" means different things to different LLMs on different days.

TRL sentences have exactly one meaning. `AGENT SHALL VALIDATE ALL CODE BEFORE COMMIT` compiles to a graph with a specific obligation, a specific action, and a specific scope. The LLM doesn't interpret — it executes.

## Examples

See [EXAMPLES/](EXAMPLES/) for real AAA plans, memory files, and TRL specifications from production use.

## Full Specification

- **TRL + TRUGS**: https://github.com/TRUGS-LLC/TRUGS
- **Paper**: https://github.com/TRUGS-LLC/TRUGS/blob/main/PAPER/trugs.pdf
- **DOI**: https://doi.org/10.5281/zenodo.19379454

## License

Apache 2.0 — TRUGS LLC
