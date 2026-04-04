# EPIC — Agent Instructions

<trl>
DEFINE "EPIC" AS DATA graph 'for RECORD project_tracking.
DATA graph EPIC CONTAINS DATA node 'of TYPE TRACKER AND TYPE EPIC AND TYPE TASK.
DATA graph EPIC CONTAINS DATA edge 'of RELATION BLOCKS AND RELATION DEPENDS_ON AND RELATION IMPLEMENTS.
AGENT SHALL READ DATA graph EPIC 'at ENTRY RECORD session.
AGENT SHALL UPDATE DATA graph EPIC WHEN RECORD status CHANGES.
</trl>

An EPIC is a TRUG graph that tracks your portfolio — projects, tasks, dependencies, and status. You read it to know what exists, what's in progress, what's blocked, and what to work on next.

---

## Structure

<trl>
DEFINE "TRACKER" AS DATA node 'at KILO METRIC_LEVEL.
DEFINE "EPIC" AS DATA node 'at HECTO METRIC_LEVEL.
DEFINE "TASK" AS DATA node 'at BASE METRIC_LEVEL.
TRACKER CONTAINS EPIC.
EPIC CONTAINS TASK.
EACH TASK SHALL CONTAIN RECORD status AND RECORD priority.
</trl>

Three levels:

```
TRACKER (root — the whole portfolio)
  └── EPIC (initiative — a body of related work)
       └── TASK (work item — one thing to do)
```

### TRACKER Node

<trl>
EACH DATA graph EPIC SHALL CONTAIN EXACTLY A DATA node 'of TYPE TRACKER.
TRACKER SHALL CONTAIN RECORD name AND RECORD owner AND RECORD total_open_issues AND RECORD last_updated.
TRACKER SHALL CONTAIN RECORD present_plan 'with RECORD summary AND RECORD active_issues.
</trl>

The root node. One per project. Contains the current focus and open issue count. This is the first thing you read.

### EPIC Node

<trl>
EACH EPIC SHALL CONTAIN RECORD name AND RECORD purpose AND RECORD status.
RECORD status SHALL 'be "TODO" OR "IN_PROGRESS" OR "DONE" OR "BLOCKED".
EPIC MAY CONTAIN RECORD github_issue AND RECORD labels AND RECORD created_date.
EACH EPIC SHALL CONTAIN ONE OR MORE TASK.
</trl>

An initiative — a group of related tasks toward a goal. Has a purpose (why it exists) and a status.

### TASK Node

<trl>
EACH TASK SHALL CONTAIN RECORD name AND RECORD status AND RECORD priority.
RECORD priority SHALL 'be "P0" OR "P1" OR "P2" OR "P3".
TASK MAY CONTAIN RECORD github_issue AND RECORD assignee.
</trl>

A single work item. Has a priority and a status. Maps to a GitHub issue when one exists.

---

## Edges

<trl>
DEFINE "BLOCKS" AS DATA edge — TARGET SHALL_NOT START UNTIL SOURCE 'is DONE.
DEFINE "DEPENDS_ON" AS DATA edge — TARGET REQUIRES SOURCE TO FUNCTION.
DEFINE "IMPLEMENTS" AS DATA edge — TARGET DELIVERS SOURCE.
EACH DATA edge SHALL CONTAIN RECORD from_id AND RECORD to_id AND RECORD relation.
DATA edge MAY CONTAIN RECORD description.
</trl>

| Relation | Meaning | Example |
|----------|---------|---------|
| `BLOCKS` | Can't start B until A is done | "Deploy" BLOCKS "Test in production" |
| `DEPENDS_ON` | B requires A to function | "API" DEPENDS_ON "Auth module" |
| `IMPLEMENTS` | B delivers A | Task IMPLEMENTS Epic |

---

## Reading the EPIC

<trl>
AGENT SHALL READ DATA graph EPIC 'at ENTRY RECORD session.
AGENT SHALL IDENTIFY ALL TASK 'where RECORD status EQUALS "IN_PROGRESS".
AGENT SHALL IDENTIFY ALL TASK 'where RECORD status EQUALS "BLOCKED".
AGENT SHALL IDENTIFY ALL DATA edge 'of RELATION BLOCKS TO UNDERSTAND RECORD dependency.
AGENT SHALL READ RECORD present_plan FROM TRACKER TO UNDERSTAND RECORD current_focus.
</trl>

At session start, read the EPIC to answer:
1. **What's the current focus?** → `tracker.present_plan.summary`
2. **What's in progress?** → all tasks with status `IN_PROGRESS`
3. **What's blocked and by what?** → follow `BLOCKS` edges
4. **What should I work on next?** → highest priority `TODO` task that isn't blocked

---

## Updating the EPIC

<trl>
IF AGENT START TASK THEN AGENT SHALL SET RECORD status TO "IN_PROGRESS".
IF AGENT COMPLETE TASK THEN AGENT SHALL SET RECORD status TO "DONE".
IF TASK 'is BLOCKED THEN AGENT SHALL SET RECORD status TO "BLOCKED" AND CREATE DATA edge 'of RELATION BLOCKS.
IF AGENT CREATE RECORD issue THEN AGENT SHALL CREATE TASK 'in EPIC 'with RECORD github_issue.
AGENT SHALL UPDATE RECORD last_updated 'on TRACKER AFTER EACH CHANGE.
AGENT SHALL UPDATE RECORD total_open_issues 'on TRACKER AFTER EACH CHANGE.
</trl>

Keep the EPIC in sync with reality:
- Start a task → mark IN_PROGRESS
- Finish a task → mark DONE
- Hit a blocker → mark BLOCKED + add BLOCKS edge
- Create a GitHub issue → add a TASK node with the issue number
- Any change → update `last_updated` and `total_open_issues` on the tracker

---

## Creating an EPIC from Scratch

<trl>
AGENT SHALL SCAN NAMESPACE project 'for ALL RECORD initiative.
'for EACH RECORD initiative AGENT SHALL CREATE DATA node 'of TYPE EPIC.
'for EACH RECORD work_item AGENT SHALL CREATE DATA node 'of TYPE TASK.
AGENT SHALL CREATE DATA edge 'for EACH RECORD dependency 'between TASK.
AGENT SHALL VALIDATE DATA graph EPIC.
</trl>

1. Identify the major initiatives (epics)
2. Break each into tasks
3. Map dependencies as BLOCKS/DEPENDS_ON edges
4. Set priorities and statuses
5. Validate the graph

See [EXAMPLE_project.trug.json](EXAMPLE_project.trug.json) for a starter template.
