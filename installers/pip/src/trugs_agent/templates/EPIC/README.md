# EPIC — Portfolio Tracker

An EPIC is a TRUG graph that tracks your projects, tasks, and their dependencies. Your LLM reads it to know what's in progress, what's blocked, and what to work on next.

## When to Use

When you have more than one initiative happening at once. The EPIC gives your LLM a bird's-eye view of all work — no more re-explaining context every session.

## How It Works

An EPIC is a `.trug.json` file with three levels:

```
TRACKER (root)
  └── EPIC (initiative)
       └── TASK (work item)
```

Edges express dependencies: `BLOCKS`, `DEPENDS_ON`, `IMPLEMENTS`.

Your LLM reads the EPIC at session start to understand:
- What projects exist and their status
- What tasks are TODO, IN_PROGRESS, or DONE
- What's blocked and by what
- What the current focus is

## Key Rule

The EPIC is the single source of truth for project state. When your LLM needs to know "what should I work on?", it reads the EPIC — not a chat history, not a TODO list.

## Example

See [EXAMPLE_project.trug.json](EXAMPLE_project.trug.json) — a starter tracker with epics, tasks, and BLOCKS dependency edges. Copy it, replace the placeholder content, and your LLM has a project map.
