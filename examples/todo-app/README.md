# Example: Todo App with TRUGS Agent

A minimal Python project showing TRUGS Agent integrated into a real codebase. This example demonstrates:

- TRL instructions in `CLAUDE.md` that govern agent behavior
- A `folder.trug.json` that indexes the project structure
- TRL annotations in Python code comments
- How TRL obligations translate to actual code behavior

## Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | TRL instructions for Claude Code (copied from root AGENT.md + project-specific rules) |
| `folder.trug.json` | Machine-readable project index |
| `app.py` | Todo app with TRL-annotated functions |

## Try It

1. Open this directory in Claude Code (or Cursor with `.cursorrules`)
2. Ask your LLM: "Read CLAUDE.md and explain the TRL instructions"
3. Ask: "Add a `delete_todo` function following the TRL specification in app.py"
4. Watch it follow the formal obligations instead of guessing
