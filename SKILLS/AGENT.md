# Skills — Agent Instructions

<trl>
DEFINE "Skill" AS FUNCTION.
EACH FUNCTION Skill CONTAINS RECORD name AND RECORD description AND RECORD input AND RECORD output.
AGENT SHALL EXECUTE FUNCTION Skill WHEN PARTY human REQUESTS RECORD name.
EACH FUNCTION Skill SHALL EXECUTE STRICTLY A RECORD specification.
EACH FUNCTION Skill SHALL PRODUCE RECORD output THEN RESPOND TO PARTY human.
</trl>

Skills are named actions an agent can execute on command. Each skill has one job, one input, one output. Primitives do one thing. Compounds sequence primitives with HITM gates between stages.

---

## Primitive vs Compound

<trl>
DEFINE "primitive" AS FUNCTION 'that CONTAINS EXACTLY A RECORD action.
DEFINE "compound" AS FUNCTION 'that CONTAINS MULTIPLE FUNCTION primitive SEQUENTIAL.
EACH FUNCTION primitive SHALL PRODUCE RECORD output THEN RESPOND TO PARTY human.
EACH FUNCTION compound SHALL EXECUTE EACH FUNCTION primitive SEQUENTIAL.
FUNCTION compound MAY REQUIRE PARTY human APPROVE RESULT 'at RECORD hitm_gate 'between FUNCTION primitive.
</trl>

A **primitive** does one atomic thing — read a file, run a command, write a node, send an email. It cannot be decomposed further.

A **compound** sequences primitives. Between stages, it may pause for human approval (HITM gate). Compounds are how agents perform multi-step workflows autonomously.

The rule: if a skill contains `THEN`, it is compound. If it does not, it is primitive.

---

## Primitive Skills

### Git Primitives

<trl>
DEFINE "git-status" AS FUNCTION.
FUNCTION git-status SHALL READ DATA working_tree THEN RESPOND 'with RECORD uncommitted AND RECORD unpushed.
</trl>

Reports uncommitted changes and unpushed commits. No side effects.

<trl>
DEFINE "git-commit" AS FUNCTION.
FUNCTION git-commit SHALL REQUIRE RECORD message FROM PARTY human.
FUNCTION git-commit SHALL WRITE ALL RECORD staged_change TO DATA repository 'with RECORD message.
FUNCTION git-commit SHALL_NOT WRITE TO ENDPOINT main.
FUNCTION git-commit SHALL_NOT WRITE TO ENDPOINT master.
</trl>

Stage, commit, and push changes on the current branch. Never commits to main.

<trl>
DEFINE "git-pr" AS FUNCTION.
FUNCTION git-pr SHALL CREATE RESOURCE pull_request FROM RECORD branch TO ENDPOINT main.
FUNCTION git-pr SHALL SEND RESOURCE pull_request TO PARTY human THEN EXIT.
PARTY human SHALL APPROVE RESOURCE pull_request THEN MERGE RESULT TO ENDPOINT main.
AGENT SHALL_NOT MERGE RESOURCE pull_request.
</trl>

Create a pull request and return the URL. The agent stops — only the human merges.

<trl>
DEFINE "git-branch" AS FUNCTION.
FUNCTION git-branch SHALL CREATE RESOURCE branch FROM ENDPOINT main.
FUNCTION git-branch SHALL REQUIRE RECORD name 'that CONTAINS RECORD issue_number OR RECORD description.
</trl>

Create a feature branch from main. Branch name includes the issue number when one exists.

---

### GitHub Primitives

<trl>
DEFINE "gh-issues" AS FUNCTION.
FUNCTION gh-issues SHALL READ ALL RECORD issue FROM ENDPOINT github 'with RECORD state AND RECORD count.
FUNCTION gh-issues MAY READ A RECORD issue BY RECORD number THEN RESPOND 'with RECORD title AND RECORD state AND RECORD labels.
</trl>

List open issues with count, or view a single issue by number.

<trl>
DEFINE "gh-prs" AS FUNCTION.
FUNCTION gh-prs SHALL READ ALL RESOURCE pull_request FROM ENDPOINT github 'with RECORD state.
FUNCTION gh-prs MAY READ RECORD diff FROM A RESOURCE pull_request BY RECORD number.
</trl>

List pull requests (open or merged), or get the file diff from a specific PR.

---

### TRUG Graph Primitives

<trl>
DEFINE "trug-sync" AS FUNCTION.
FUNCTION trug-sync SHALL READ DATA filesystem THEN WRITE RECORD node 'for EACH NEW FILE TO FILE folder.trug.json.
FUNCTION trug-sync SHALL VALIDATE EACH RECORD node SUBJECT_TO DATA filesystem.
FUNCTION trug-sync SHALL MARK RECORD node AS PENDING IF FILE 'is 'not FOUND.
FUNCTION trug-sync SHALL_NOT REPLACE ANY RECORD node.
</trl>

Run `tg sync` on a folder. Adds nodes for new files, marks missing files stale. Never removes nodes.

<trl>
DEFINE "trug-check" AS FUNCTION.
FUNCTION trug-check SHALL VALIDATE FILE folder.trug.json SUBJECT_TO RECORD rule.
FUNCTION trug-check SHALL RESPOND 'with RECORD result AS VALID OR INVALID.
IF RECORD result 'is INVALID THEN FUNCTION trug-check SHALL RESPOND 'with EACH RECORD error.
</trl>

Run `tg check` to validate a folder.trug.json against structural rules. Returns pass/fail with error details.

<trl>
DEFINE "trug-clean" AS FUNCTION.
FUNCTION trug-clean SHALL READ FILE folder.trug.json THEN FILTER ALL RECORD edge 'where RECORD from_id OR RECORD to_id 'is INVALID.
FUNCTION trug-clean SHALL FILTER ALL RECORD node 'where RECORD stale EQUALS BOOLEAN 'true AND NO RECORD edge REFERENCES RECORD node.
FUNCTION trug-clean SHALL VALIDATE EACH RECORD path SUBJECT_TO DATA filesystem.
FUNCTION trug-clean SHALL MARK RECORD node AS PENDING IF RECORD path 'is INVALID.
PARTY human SHALL APPROVE RESULT 'before FUNCTION trug-clean SHALL WRITE TO FILE folder.trug.json.
</trl>

Remove orphaned edges (dangling references), remove dead stale nodes (no remaining edges), mark nodes with broken paths. Presents findings for HITM approval before saving.

<trl>
DEFINE "trug-edge" AS FUNCTION.
FUNCTION trug-edge SHALL REQUIRE RECORD from_file.
FUNCTION trug-edge MAY REQUIRE RECORD to_file AND RECORD relation.
IF RECORD to_file 'is 'not PROVIDED THEN FUNCTION trug-edge SHALL READ RECORD from_file THEN RESPOND 'with EACH RECORD proposed_edge.
PARTY human SHALL APPROVE EACH RECORD proposed_edge 'before WRITE.
FUNCTION trug-edge SHALL WRITE RECORD edge TO FILE folder.trug.json.
</trl>

Add or infer edges. Three modes: smart (one file — infer everything), directed (two files — infer relation), explicit (all three specified). Always asks for approval in smart/directed mode.

---

### Memory Primitives

<trl>
DEFINE "memory-save" AS FUNCTION.
FUNCTION memory-save SHALL REQUIRE RECORD content AND RECORD type AND RECORD name.
RECORD type 'is "user" OR "feedback" OR "project" OR "reference".
FUNCTION memory-save SHALL WRITE FILE memory_record TO NAMESPACE memory.
FUNCTION memory-save SHALL WRITE RECORD pointer TO FILE MEMORY.md.
</trl>

Write a memory file with frontmatter (name, description, type) and add a one-line pointer to MEMORY.md. One memory per call.

<trl>
DEFINE "memory-read" AS FUNCTION.
FUNCTION memory-read SHALL READ FILE MEMORY.md THEN RESPOND 'with RECORD index.
FUNCTION memory-read MAY READ FILE memory_record BY RECORD name.
</trl>

Read the memory index or a specific memory file. Used at session start to load context.

---

### EPIC Primitives

<trl>
DEFINE "epic-read" AS FUNCTION.
FUNCTION epic-read SHALL READ FILE project.trug.json THEN RESPOND 'with DATA present_plan AND DATA portfolio_status AND DATA critical_path.
FUNCTION epic-read MAY READ FILE epic.trug.json 'for RECORD business_context.
</trl>

Read the EPIC tracker — present plan, critical path, active issues, portfolio status. Optionally reads business epic if accessible.

<trl>
DEFINE "epic-sync" AS FUNCTION.
FUNCTION epic-sync SHALL READ EACH RECORD task FROM FILE project.trug.json.
FUNCTION epic-sync SHALL VALIDATE EACH RECORD task SUBJECT_TO ENDPOINT github 'by RECORD issue_number.
IF RECORD task RECORD status 'is INVALID THEN FUNCTION epic-sync SHALL WRITE RECORD status TO FILE project.trug.json.
</trl>

Sync EPIC task node statuses with GitHub issue states. Updates status, pr_number, completed_date for any task that has drifted from reality.

<trl>
DEFINE "epic-portfolio" AS FUNCTION.
FUNCTION epic-portfolio SHALL READ DATA filesystem THEN VALIDATE EACH RECORD folder SUBJECT_TO DATA portfolio_status.
IF RECORD folder 'is NEW THEN FUNCTION epic-portfolio SHALL WRITE RECORD folder TO DATA portfolio_status.
IF RECORD folder RECORD phase 'is INVALID THEN FUNCTION epic-portfolio SHALL WRITE RECORD phase.
</trl>

Update the portfolio_status node in the EPIC. Adds new top-level folders, updates phase for modified folders, verifies TRACKED_BY edges.

---

### Decision Primitive

<trl>
DEFINE "decisions" AS FUNCTION.
FUNCTION decisions SHALL READ DATA conversation THEN FILTER ALL RECORD decision.
RECORD decision 'is RECORD architecture_choice OR RECORD rule_change OR RECORD assumption_change OR RECORD surprising_finding OR RECORD priority_change.
RECORD decision 'is 'not RECORD routine_code_change OR RECORD bug_fix OR RECORD file_rename.
FUNCTION decisions SHALL RESPOND 'with EACH RECORD decision TO PARTY human.
PARTY human SHALL APPROVE EACH RECORD decision 'before FUNCTION memory-save SHALL EXECUTE.
</trl>

Mine the current conversation for key decisions — architecture choices, new rules, changed assumptions, surprising findings, scope changes. Present to the human for approval, then save each approved decision via `/memory-save`.

---

### Worktree Primitives

<trl>
DEFINE "worktree-create" AS FUNCTION.
FUNCTION worktree-create SHALL REQUIRE RECORD issue_number.
FUNCTION worktree-create SHALL CREATE RESOURCE worktree FROM ENDPOINT main 'for RECORD issue_number.
FUNCTION worktree-create SHALL_NOT REPLACE ANY RESOURCE worktree.
</trl>

Create a git worktree for an issue. Each worktree gets its own directory and branch — isolated git state for concurrent development.

<trl>
DEFINE "worktree-list" AS FUNCTION.
FUNCTION worktree-list SHALL READ ALL RESOURCE worktree THEN RESPOND 'with EACH RECORD path AND RECORD branch AND RECORD status.
</trl>

List all active worktrees with their branch and dirty/clean status.

<trl>
DEFINE "worktree-remove" AS FUNCTION.
FUNCTION worktree-remove SHALL REQUIRE RECORD issue_number.
IF RESOURCE worktree CONTAINS RECORD uncommitted_change THEN PARTY human SHALL APPROVE 'before FUNCTION worktree-remove SHALL EXECUTE.
FUNCTION worktree-remove SHALL REMOVE RESOURCE worktree 'for RECORD issue_number.
</trl>

Remove a worktree. Warns and asks for approval if uncommitted changes exist.

---

## Compound Skills — Composition

<trl>
DEFINE "compound" AS FUNCTION 'that CONTAINS MULTIPLE FUNCTION primitive SEQUENTIAL.
EACH FUNCTION compound SHALL DECLARE EACH FUNCTION primitive 'it CONTAINS.
FUNCTION compound MAY DEFINE RECORD hitm_gate 'between ANY FUNCTION primitive.
RECORD hitm_gate SHALL REQUIRE PARTY human APPROVE RESULT 'before FUNCTION compound CONTINUES.
</trl>

A compound skill is a declared sequence of primitives. HITM gates are inserted where the human must approve before the agent continues. The compound skill definition IS the sequence — no hidden logic.

---

### Example: `/session-open`

<trl>
DEFINE "session-open" AS FUNCTION compound.
FUNCTION session-open CONTAINS FUNCTION memory-read THEN FUNCTION epic-read THEN FUNCTION gh-issues THEN FUNCTION gh-prs THEN FUNCTION worktree-list.
FUNCTION memory-read SHALL READ RECORD session_summary FROM NAMESPACE memory.
FUNCTION epic-read SHALL READ DATA present_plan FROM FILE project.trug.json.
FUNCTION gh-issues SHALL READ RECORD count FROM ENDPOINT github.
FUNCTION gh-prs SHALL READ ALL RESOURCE pull_request 'with RECORD state 'is "open".
FUNCTION worktree-list SHALL READ ALL RESOURCE worktree.
FUNCTION session-open SHALL RESPOND TO PARTY human 'with RECORD overview AND RECORD suggested_next_steps.
PARTY human SHALL APPROVE RECORD direction 'before AGENT CONTINUES.
</trl>

**Sequence:** Load last session from memory. Read EPIC for current plan and priorities. Count open issues. List open PRs. List worktrees. Present overview and suggest next steps. Wait for the human to choose direction.

---

### Example: `/session-update`

<trl>
DEFINE "session-update" AS FUNCTION compound.
FUNCTION session-update CONTAINS FUNCTION git-status THEN FUNCTION git-commit THEN FUNCTION decisions THEN FUNCTION memory-save THEN FUNCTION trug-edge THEN FUNCTION epic-sync THEN FUNCTION epic-portfolio THEN FUNCTION trug-sync THEN FUNCTION git-commit THEN FUNCTION git-pr.
FUNCTION git-status SHALL READ DATA working_tree.
IF DATA working_tree CONTAINS RECORD uncommitted_change THEN FUNCTION git-commit SHALL EXECUTE.
FUNCTION decisions SHALL READ DATA conversation THEN RESPOND 'with EACH RECORD decision.
RECORD hitm_gate SHALL REQUIRE PARTY human APPROVE EACH RECORD decision.
FUNCTION memory-save SHALL WRITE EACH RECORD decision TO NAMESPACE memory.
FUNCTION trug-edge SHALL READ EACH RECORD merged_pr THEN WRITE RECORD edge TO FILE folder.trug.json.
FUNCTION epic-sync SHALL VALIDATE EACH RECORD task SUBJECT_TO ENDPOINT github.
FUNCTION epic-portfolio SHALL VALIDATE DATA portfolio_status SUBJECT_TO DATA filesystem.
FUNCTION trug-sync SHALL EXECUTE 'on EACH RECORD modified_folder.
FUNCTION git-commit SHALL WRITE ALL RECORD change 'with RECORD message "chore(maintenance)".
FUNCTION git-pr SHALL CREATE RESOURCE pull_request THEN SEND TO PARTY human.
</trl>

**Sequence:** Check for uncommitted work — commit and push if needed. Mine conversation for decisions — present for HITM approval. Save approved decisions to memory. Create edges from merged PRs to code nodes. Sync EPIC task statuses with GitHub. Update portfolio status. Run folder-sync on modified folders. Commit all maintenance changes. Create PR — human merges.

---

### Example: `/session-close`

<trl>
DEFINE "session-close" AS FUNCTION compound.
FUNCTION session-close CONTAINS FUNCTION session-update THEN FUNCTION memory-save THEN FUNCTION trug-clean THEN FUNCTION epic-sync THEN FUNCTION trug-check THEN FUNCTION worktree-remove THEN FUNCTION git-commit THEN FUNCTION git-pr.
FUNCTION session-update SHALL EXECUTE 'without FUNCTION git-pr.
FUNCTION memory-save SHALL WRITE RECORD session_summary TO NAMESPACE memory.
FUNCTION trug-clean SHALL EXECUTE 'on ALL FILE folder.trug.json.
RECORD hitm_gate SHALL REQUIRE PARTY human APPROVE RESULT 'of FUNCTION trug-clean.
FUNCTION epic-sync SHALL WRITE RECORD total_open_issues AND RECORD last_updated TO FILE project.trug.json.
FUNCTION trug-check SHALL VALIDATE ALL FILE folder.trug.json THEN RESPOND 'with RECORD result.
FUNCTION worktree-remove SHALL REMOVE EACH RESOURCE worktree 'where RECORD branch 'is MERGED.
FUNCTION git-commit SHALL WRITE ALL RECORD change 'with RECORD message "chore(stop)".
FUNCTION git-pr SHALL CREATE RESOURCE pull_request THEN SEND TO PARTY human.
</trl>

**Sequence:** Run full session-update (without its own PR). Write session summary to memory. Clean all TRUG graphs — remove orphaned edges, stale nodes, broken paths (HITM gate). Sync EPIC issue counts. Validate all TRUGs. Remove merged worktrees. Commit everything. Create single PR — human merges.

---

## Building New Compounds

<trl>
AGENT MAY DEFINE NEW FUNCTION compound BY COMPOSE EXISTING FUNCTION primitive.
EACH NEW FUNCTION compound SHALL DECLARE EACH FUNCTION primitive 'it CONTAINS.
EACH NEW FUNCTION compound SHALL DEFINE RECORD hitm_gate 'where PARTY human APPROVAL 'is REQUIRED.
AGENT SHALL_NOT DEFINE FUNCTION primitive 'that CONTAINS FUNCTION primitive.
AGENT MAY DEFINE FUNCTION compound 'that CONTAINS FUNCTION compound.
</trl>

To create a new compound skill:

1. Identify the primitives you need from the catalog above
2. Declare the sequence with `CONTAINS ... THEN ... THEN ...`
3. Insert HITM gates where the human must approve before continuing
4. A primitive never contains another primitive — it is atomic
5. A compound may contain other compounds (nesting is allowed)

### Example: Building a hypothetical `/deploy-check`

<trl>
DEFINE "deploy-check" AS FUNCTION compound.
FUNCTION deploy-check CONTAINS FUNCTION trug-check THEN FUNCTION trug-sync THEN FUNCTION epic-sync THEN FUNCTION git-status.
FUNCTION trug-check SHALL VALIDATE ALL FILE folder.trug.json.
IF RECORD result 'is INVALID THEN FUNCTION deploy-check SHALL RESPOND 'with EACH RECORD error THEN EXIT.
FUNCTION trug-sync SHALL EXECUTE 'on ALL RECORD folder.
FUNCTION epic-sync SHALL VALIDATE EACH RECORD task SUBJECT_TO ENDPOINT github.
FUNCTION git-status SHALL VALIDATE NO RECORD uncommitted_change EXISTS.
FUNCTION deploy-check SHALL RESPOND 'with RECORD ready AS BOOLEAN.
</trl>

**Sequence:** Validate all TRUGs — stop if any fail. Sync all folders. Sync EPIC with GitHub. Verify no uncommitted changes. Report ready/not-ready.

---

## Skill File Format

<trl>
EACH FUNCTION Skill SHALL 'be DEFINED 'in FILE SKILL.md 'in NAMESPACE .claude/skills/RECORD name/.
FILE SKILL.md SHALL CONTAIN RECORD frontmatter 'with RECORD name AND RECORD description.
FILE SKILL.md SHALL CONTAIN RECORD specification 'that GOVERNS AGENT EXECUTION.
</trl>

Each skill lives at `.claude/skills/<name>/SKILL.md`. The file contains:

1. **Frontmatter** — name and one-line description
2. **Specification** — the exact steps the agent executes

```markdown
---
name: skill-name
description: One-line description of what the skill does
---

# /skill-name — Title

Steps the agent executes...
```

The human invokes a skill by typing `/<name>` in the conversation. The agent loads the SKILL.md and executes strictly what it specifies.
