# Skills — Composable Agent Actions

Skills are named actions your LLM executes on command. Type `/skill-name` and the agent does exactly what the skill specifies.

## How It Works

Two kinds of skills:

| Kind | Rule | Example |
|------|------|---------|
| **Primitive** | One action, one output, no decomposition | `/git-status`, `/trug-check`, `/email-fetch` |
| **Compound** | Sequence of primitives with HITM gates | `/session-open`, `/session-close`, `/email-triage` |

## The 19 Primitives

| Category | Skills |
|----------|--------|
| **Git** | `git-status`, `git-commit`, `git-pr`, `git-branch` |
| **GitHub** | `gh-issues`, `gh-prs` |
| **TRUG Graph** | `trug-sync`, `trug-check`, `trug-clean`, `trug-edge` |
| **Memory** | `memory-save`, `memory-read` |
| **EPIC** | `epic-read`, `epic-sync`, `epic-portfolio` |
| **Decisions** | `decisions` |
| **Worktree** | `worktree-create`, `worktree-list`, `worktree-remove` |

## Compound Examples

```
/session-open  = memory-read > epic-read > gh-issues > gh-prs > worktree-list
/session-update = git-status > git-commit > decisions > memory-save > trug-edge > epic-sync > epic-portfolio > trug-sync > git-commit > git-pr
/session-close = session-update > memory-save > trug-clean > epic-sync > trug-check > worktree-remove > git-commit > git-pr
```

The `>` means "then." Where a human must approve before continuing, the compound inserts a HITM gate.

## Key Rule

Primitives are atomic — they never contain other primitives. Compounds sequence primitives. You can build new compounds by composing existing primitives. You can nest compounds inside other compounds.

## Full Specification

See [AGENT.md](AGENT.md) for the complete TRL definitions of all 19 primitives and 3 compound examples.
