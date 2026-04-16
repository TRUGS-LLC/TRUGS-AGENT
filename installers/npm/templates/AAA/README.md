# AAA — 9-Phase Development Protocol

AAA is a development workflow that forces your LLM to plan before it codes, define "done" before it builds, and never ship without your approval.

## When to Use

Any time your LLM needs to build something non-trivial. If the task has unknowns, needs design decisions, or touches multiple files — use AAA.

For simple, known tasks (fix a typo, rename a variable), skip AAA entirely and use a CHORE: branch, do it, PR, merge.

## How It Works

**Two cycles, three human touchpoints:**

```
PLANNING: VISION → FEASIBILITY → SPECIFICATIONS → ARCHITECTURE → VALIDATION (human approves)
EXECUTION: CODING → TESTING → AUDIT → DEPLOYMENT (human merges)
```

1. **You** state what you want (VISION)
2. **Agent** plans it (phases 2-4), including audit criteria in phase 3
3. **You** approve the plan (VALIDATION)
4. **Agent** builds and tests it (phases 6-8), auditing against phase 3 criteria
5. **You** merge the PR (DEPLOYMENT)

The agent never codes without an approved plan. Never ships without your review.

## Key Rule

Phase 3 (SPECIFICATIONS) defines the audit criteria. Phase 8 (AUDIT) checks against them. The plan defines what "done" looks like before any code is written.

## Example

See [EXAMPLE_email_mcp.md](EXAMPLE_email_mcp.md) — a real AAA plan from building an email MCP server. All 9 phases, TRUG/L specs, audit criteria, and coding plan.
