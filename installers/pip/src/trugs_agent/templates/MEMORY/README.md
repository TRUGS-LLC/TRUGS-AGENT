# Memory — Persistent Context Across Sessions

Memory lets your LLM remember decisions, preferences, and project state between conversations. No more repeating yourself.

## When to Use

Every project benefits from memory. It's lightweight — a few markdown files that accumulate over time.

## How It Works

Memory is a folder of markdown files indexed by `MEMORY.md`:

```
MEMORY/
  MEMORY.md              ← Index (one-line pointers)
  user_role.md           ← Who you are
  feedback_no_mocks.md   ← What you've corrected
  project_freeze.md      ← What's happening
  reference_linear.md    ← Where to find things
```

Four memory types:

| Type | Save When | Example |
|------|-----------|---------|
| **user** | You learn about their role or preferences | "Senior backend engineer, new to React" |
| **feedback** | They correct or confirm an approach | "Don't mock the database in tests" |
| **project** | You learn who/what/why/when | "Merge freeze starts March 5" |
| **reference** | You learn about external resources | "Bugs tracked in Linear project INGEST" |

Your LLM reads `MEMORY.md` at session start. Saves new memories when decisions are made. Updates stale memories when things change.

## Key Rule

Memory stores what can't be derived from code or git history. Don't save file paths, architecture, or code patterns — those belong in the code. Save the *why* behind decisions, user preferences, and pointers to external systems.

## Example

See [EXAMPLE_MEMORY.md](EXAMPLE_MEMORY.md) for a starter index and the format for individual memory files.
