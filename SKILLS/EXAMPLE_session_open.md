# Example Compound Skill: `/session-open`

This file demonstrates how a compound skill chains primitives with HITM gates.

## TRL Definition

<trl>
DEFINE "session-open" AS FUNCTION compound.
FUNCTION session-open CONTAINS FUNCTION memory-read THEN FUNCTION epic-read THEN FUNCTION gh-issues THEN FUNCTION gh-prs THEN FUNCTION worktree-list.
FUNCTION memory-read SHALL READ RECORD session_summary FROM NAMESPACE memory.
FUNCTION epic-read SHALL READ DATA present_plan AND DATA critical_path FROM FILE project.trug.json.
FUNCTION gh-issues SHALL READ ALL RECORD issue 'with RECORD state EQUALS "open".
FUNCTION gh-prs SHALL READ ALL RESOURCE pull_request 'with RECORD state EQUALS "open".
FUNCTION worktree-list SHALL READ ALL RESOURCE worktree THEN RESPOND 'with EACH RECORD path AND RECORD branch.
FUNCTION session-open SHALL RESPOND TO PARTY human 'with RECORD overview AND RECORD suggested_next_steps.
RECORD hitm_gate SHALL REQUIRE PARTY human APPROVE RECORD direction 'before AGENT CONTINUES.
</trl>

## Chain

```
/session-open = memory-read > epic-read > gh-issues > gh-prs > worktree-list
                                                                     |
                                                              [HITM: human chooses direction]
```

## Step-by-Step

| # | Primitive | What It Does |
|---|-----------|-------------|
| 1 | `memory-read` | Load last session summary from `MEMORY.md` |
| 2 | `epic-read` | Read `project.trug.json` for present plan, critical path, active issues |
| 3 | `gh-issues` | Count open issues, list labels and assignees |
| 4 | `gh-prs` | List open PRs with review status |
| 5 | `worktree-list` | Show active worktrees, their branches, and dirty/clean status |

## HITM Gate

After all 5 primitives complete, the agent presents:
- **Overview** — what happened last session, what is in flight, what is blocked
- **Suggested next steps** — ranked by critical path priority

The human approves a direction before the agent begins work. This is the single HITM gate in `/session-open`.

## Key Rules

- Primitives execute **sequentially** (`THEN` chains, not `AND`)
- Each primitive produces one output consumed by the overview
- The compound itself produces no side effects — it is read-only
- The HITM gate is at the **end**, not between primitives
