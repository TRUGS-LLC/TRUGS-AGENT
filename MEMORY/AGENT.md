# Memory — Agent Instructions

<trl>
DEFINE "Memory" AS MODULE CONTAINS RECORD user AND RECORD feedback AND RECORD project AND RECORD reference.
AGENT SHALL READ FILE MEMORY.md 'at ENTRY RECORD session.
AGENT SHALL WRITE RECORD decision TO MODULE Memory DURING RECORD session.
AGENT SHALL WRITE RECORD summary TO MODULE Memory 'at EXIT RECORD session.
</trl>

Memory is how you persist context across sessions. Decisions, preferences, project state, and pointers to external systems — stored as markdown files, indexed by MEMORY.md.

---

## Memory Types

<trl>
DEFINE "user" AS RECORD 'for PARTY human CONTAINS RECORD role AND RECORD preference AND RECORD expertise.
DEFINE "feedback" AS RECORD 'for RECORD correction OR RECORD confirmation.
DEFINE "project" AS RECORD 'for RECORD decision OR RECORD status OR RECORD deadline.
DEFINE "reference" AS RECORD 'for ENDPOINT external_system.
</trl>

| Type | Save When | Example |
|------|-----------|---------|
| **user** | You learn about their role or preferences | "User is a data scientist focused on observability" |
| **feedback** | They correct you OR confirm a non-obvious approach | "Don't mock the database — use real DB in tests" |
| **project** | You learn who does what, why, or by when | "Merge freeze 2026-03-05 for mobile release" |
| **reference** | You learn about external resources | "Pipeline bugs tracked in Linear project INGEST" |

### User Memories

<trl>
AGENT SHALL WRITE RECORD user WHEN AGENT LEARN RECORD role OR RECORD preference OR RECORD expertise 'of PARTY human.
RECORD user SHALL HELP AGENT TAILOR RECORD response TO PARTY human.
</trl>

Who the human is. Their role, expertise, how they like to work. A senior engineer gets different explanations than a student. A backend developer gets frontend concepts explained through backend analogies.

### Feedback Memories

<trl>
AGENT SHALL WRITE RECORD feedback WHEN PARTY human CORRECT RECORD approach.
AGENT SHALL WRITE RECORD feedback WHEN PARTY human CONFIRM RECORD non_obvious_approach.
EACH RECORD feedback SHALL CONTAIN RECORD rule AND RECORD why AND RECORD how_to_apply.
</trl>

What the human has corrected or confirmed. Both matter — corrections prevent repeating mistakes, confirmations prevent abandoning validated approaches. Always record the **why** so you can judge edge cases.

### Project Memories

<trl>
AGENT SHALL WRITE RECORD project WHEN AGENT LEARN RECORD decision OR RECORD deadline OR RECORD status.
AGENT SHALL CONVERT ALL RECORD relative_date TO RECORD absolute_date 'before WRITE.
EACH RECORD project SHALL CONTAIN RECORD fact AND RECORD why AND RECORD how_to_apply.
</trl>

What's happening in the project. Decisions, deadlines, who's doing what. Always convert relative dates ("Thursday") to absolute dates ("2026-03-05") so the memory stays useful.

### Reference Memories

<trl>
AGENT SHALL WRITE RECORD reference WHEN AGENT LEARN RECORD location 'of RECORD external_resource.
RECORD reference SHALL CONTAIN RECORD system AND RECORD purpose AND RECORD url_or_path.
</trl>

Where to find things outside the codebase. Bug trackers, dashboards, documentation, Slack channels.

---

## What NOT to Save

<trl>
NO AGENT SHALL WRITE RECORD memory 'for DATA code_pattern.
NO AGENT SHALL WRITE RECORD memory 'for DATA git_history.
NO AGENT SHALL WRITE RECORD memory 'for DATA 'that EXISTS 'in FILE CLAUDE.md.
NO AGENT SHALL WRITE RECORD memory 'for RECORD ephemeral_task.
NO AGENT SHALL WRITE RECORD memory 'for DATA file_path OR DATA architecture.
</trl>

Don't save what you can derive:
- **Code patterns** — read the code
- **Git history** — run git log
- **File paths** — use glob/grep
- **Architecture** — read the TRUGs
- **Ephemeral state** — current task context dies with the session
- **Anything in CLAUDE.md** — it's already loaded every session

---

## Memory File Format

<trl>
EACH RECORD memory SHALL PERSIST AS FILE 'with RECORD frontmatter AND RECORD content.
RECORD frontmatter SHALL CONTAIN RECORD name AND RECORD description AND RECORD type.
RECORD description SHALL 'be SPECIFIC — USED TO DECIDE RECORD relevance 'in FUTURE SESSION.
</trl>

```markdown
---
name: short title
description: one-line description — be specific, this decides relevance
type: user|feedback|project|reference
---

Content here.

**Why:** reason for the decision
**How to apply:** when this should influence future work
```

---

## MEMORY.md Index

<trl>
FILE MEMORY.md SHALL CONTAIN A RECORD pointer 'for EACH RECORD memory.
EACH RECORD pointer SHALL 'be LESS_THAN 150 STRING characters.
FILE MEMORY.md SHALL 'be ORGANIZED BY RECORD type.
AGENT SHALL UPDATE FILE MEMORY.md WHEN AGENT CREATE OR DELETE RECORD memory.
</trl>

MEMORY.md is an index, not a memory. One line per entry, under 150 characters. Organized by type.

```markdown
# Memory Index

## User
- [user_role.md](user_role.md) — Senior backend engineer, new to React

## Feedback
- [feedback_no_mocks.md](feedback_no_mocks.md) — Integration tests hit real DB, not mocks

## Project
- [project_freeze.md](project_freeze.md) — Merge freeze 2026-03-05 for mobile release

## Reference
- [reference_linear.md](reference_linear.md) — Pipeline bugs in Linear project "INGEST"
```

---

## Session Lifecycle

<trl>
AGENT SHALL READ FILE MEMORY.md 'at ENTRY RECORD session.
AGENT SHALL WRITE RECORD decision TO MODULE Memory WHEN RECORD decision EXISTS.
AGENT SHALL WRITE RECORD session_summary 'at EXIT RECORD session.
AGENT SHALL WRITE RECORD pointer TO FILE MEMORY.md 'for EACH NEW RECORD memory.
</trl>

### Session Start

Read MEMORY.md. Load relevant memories based on the task at hand. Don't load everything — load what's relevant.

### During Session

Save memories as they happen. When the human makes a decision, save it. When they correct you, save the feedback. Don't batch — save immediately.

### Session End

Write a session summary: what was accomplished, what decisions were made, what's left to do. Update MEMORY.md with any new entries.

---

## Memory Hygiene

<trl>
AGENT SHALL_NOT WRITE RECORD memory 'that DUPLICATES EXISTING RECORD memory.
AGENT SHALL UPDATE RECORD memory WHEN RECORD fact CHANGES.
AGENT SHALL DELETE RECORD memory WHEN RECORD fact 'is NO_LONGER VALID.
AGENT SHALL VERIFY RECORD memory 'before RECOMMEND RECORD action BASED_ON RECORD memory.
</trl>

- **No duplicates** — check before writing. Update existing memories instead.
- **Update stale memories** — facts change. When they do, update the memory.
- **Delete obsolete memories** — if a decision was reversed or a deadline passed, remove it.
- **Verify before acting** — a memory that names a file or function is a claim about the past. Check that it still exists before recommending it.

See [EXAMPLE_MEMORY.md](EXAMPLE_MEMORY.md) for a starter index.
