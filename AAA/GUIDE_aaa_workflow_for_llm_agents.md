# The AAA System: How Work Gets Specified for LLM Agents

**A complete guide to the 9-phase issue-sourced development protocol.**

**Version:** 2.0.0
**Date:** 2026-03-24  
**Audience:** Developers using LLM agents for coding, and the LLM agents themselves  
**Context:** This guide describes the AAA protocol used in TRUGS-DEVELOPMENT. No tools are required — only this process, applied consistently.

---

## The Core Problem

LLM agents need specifications, not conversations. A human can ask a colleague "hey, can you build the auth service?" and trust that the colleague will ask clarifying questions, check the codebase, and figure out details. An LLM agent receiving that instruction will either hallucinate the details or stop and ask — neither outcome is productive.

The deeper problem: where does the specification *live*? If it's scattered across Slack threads, meeting notes, half-written docs, and mental models — no agent can find it. If it's in a single document but that document is stale — the agent builds the wrong thing.

**The solution is a single source of truth for work specifications, with a lifecycle that keeps it current.** That's AAA.

---

## Two Paths — CHORE or ISSUE

Before starting any work, decide:

| Path | When | Flow |
|------|------|------|
| **CHORE** | Simple task, known steps, no unknowns | Branch → PR → merge. No issue needed. |
| **ISSUE** | Idea, proposal, feature, bug — anything with unknowns | Issue → AAA → PLANNING → HITM → EXECUTION → PR → merge |

**If it needs an issue, it needs an AAA. If it doesn't need an issue, it's a chore.** No middle ground.

<trl>
AGENT claude SHALL MATCH RECORD task AS RESOURCE chore OR RESOURCE issue.
AGENT claude SHALL_NOT DEFINE ANY RESOURCE 'that 'is RESOURCE issue UNLESS RECORD aaa EXISTS.
RESOURCE chore SHALL_NOT REQUIRE RECORD aaa.
</trl>

## What Is AAA?

AAA is a 9-phase development protocol where **GitHub Issues are the source of truth**. The issue body contains a complete specification — from vision through deployment — in a structured format that both humans and LLM agents can consume.

The name "AAA" comes from the file sorting first alphabetically in any folder listing. When an agent enters a folder and sees `AAA.md`, it knows immediately: **there is active work here with a formal specification.**

### The 9 Phases in 2 Cycles

**PLANNING cycle** — define, design, validate the plan:

| Phase | Name | Type | Purpose | Key Output |
|-------|------|------|---------|------------|
| 1 | **VISION** | Define | What and why | Problem statement, success criteria |
| 2 | **FEASIBILITY** | Decide | Quick kill — worth pursuing? | GO/NO-GO decision |
| 3 | **SPECIFICATIONS** | Define | Exact requirements | API contracts, data models, acceptance criteria |
| 4 | **ARCHITECTURE** | Design | System design | Component map, tech stack, ADRs, data flows |
| 5 | **VALIDATION** | **HITM Gate** | Audit phases 1-4 + coding plan | All checks green + human approves plan → proceed to EXECUTION |

**EXECUTION cycle** — build, test, audit, ship:

| Phase | Name | Type | Purpose | Key Output |
|-------|------|------|---------|------------|
| 6 | **CODING** | Build | Implementation | Task list, test coverage, blockers |
| 7 | **TESTING** | Verify | Run tests | Test results, bug tracking, coverage |
| 8 | **AUDIT** | **HITM Gate** | Audit code + tests. **Two categories: Code Quality + Plan Compliance.** Write tests for any finding that lacks coverage. Cycle until no critical/high. | No critical/high + human approves → proceed to DEPLOYMENT |
| 9 | **DEPLOYMENT** | Ship | Release | Deployment strategy, monitoring, runbooks |

Every phase has a **Phase Status** (`NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `BLOCKED`, `NOT_APPLICABLE`) and a **Quality Gate** (`✅` passed, `⏳` pending, `🔴` blocked).

**Three human touchpoints:** VISION (human states what they want), VALIDATION (human approves the plan), AUDIT/DEPLOYMENT (human approves the result).

<trl>
PARTY human GOVERNS STAGE vision AND STAGE validation AND STAGE deployment.
AGENT claude GOVERNS STAGE feasibility AND STAGE specifications AND STAGE architecture AND STAGE coding AND STAGE testing AND STAGE audit.
PARTY human SHALL APPROVE STAGE validation THEN AGENT claude MAY IMPLEMENT STAGE coding.
AGENT claude SHALL_NOT IMPLEMENT STAGE coding UNLESS PARTY human SHALL APPROVE STAGE validation.
AGENT claude SHALL DEFINE RESOURCE pull_request THEN SEND RESULT TO PARTY human THEN EXIT.
PARTY human SHALL APPROVE RESOURCE pull_request THEN MERGE RESULT TO ENDPOINT main.
AGENT claude SHALL_NOT MERGE ANY RESOURCE TO ENDPOINT main.
</trl>

**At scale:** PLANNING cycle runs on expensive models (Opus). EXECUTION cycle can run on cheaper models (Sonnet/Haiku) for routine tasks. The cycle boundary is the compute routing signal.

### Why 9 phases instead of just "write a spec"?

Because different questions need answering at different times. You shouldn't architect a system you haven't researched. You shouldn't code a system you haven't specified. Each phase has a quality gate that must pass before the next phase produces reliable output.

<trl>
STAGE vision FEEDS STAGE feasibility.
STAGE feasibility FEEDS STAGE specifications.
STAGE specifications FEEDS STAGE architecture.
STAGE architecture FEEDS STAGE validation.
STAGE validation FEEDS STAGE coding.
STAGE coding FEEDS STAGE testing.
STAGE testing FEEDS STAGE audit.
STAGE audit FEEDS STAGE deployment.
EACH STAGE SHALL REQUIRE RESULT FROM SOURCE STAGE EQUALS VALID.
AGENT claude SHALL_NOT IMPLEMENT ANY STAGE UNLESS SOURCE STAGE EQUALS VALID.
</trl>

For agents, this means: when Phase 3 (SPECIFICATIONS) is `COMPLETE` and Phase 5 (CODING) is `NOT_STARTED`, the agent knows exactly where it stands — the spec is ready, implementation hasn't begun. No ambiguity.

---

## The Lifecycle: From Idea to Agent Execution

### Step 1: Developer writes documents on disk

Nobody sits down and writes a complete 9-phase issue from scratch. In practice, development happens on disk first — iteratively, in sections:

```
TRUGS_COMPUTATION/
├── VISION_computation_communication_layer.md   ← Phase 1 thinking
├── RESEARCH_computation_feasibility.md         ← Phase 2 research
├── SPEC_computation.md                         ← Phase 3 specification
├── PROPOSAL_theoretical_foundations.md          ← Design exploration
├── PROPOSAL_cfg_analysis.md                    ← Alternative approach
└── PITCH_computation_layer.md                  ← Presentation material
```

These are **working artifacts**. They follow the `TYPE_description.md` naming convention so anyone — human or agent — can tell what each file is without opening it. The TYPE prefix maps to AAA phases:

| Document TYPE | AAA Phase | Purpose |
|---------------|-----------|---------|
| `VISION_` | Phase 1 | Motivation, goals, the "why" |
| `FEASIBILITY_` | Phase 2 | Can it be built? Research and analysis |
| `RESEARCH_` | Phase 2 | Detailed research (feeds feasibility) |
| `SPEC_` | Phase 3 | Formal requirements |
| `PROPOSAL_` | Phase 3-4 | Design options (feeds spec or architecture) |
| `ARCHITECTURE` | Phase 4 | System design (auto-generated from folder.trug.json) |
| `DEPLOYMENT_` | Phase 6 | Release and operations |

### Step 2: Developer writes the GitHub Issue

When the thinking is mature enough, the developer consolidates the working documents into a GitHub Issue body using the 9-phase template. The issue body becomes the **single source of truth**.

The working documents on disk either:
- Become part of the permanent record (referenced from the issue)
- Get archived with `zzz_` prefix when superseded by the issue content
- Stay as-is until the issue is completed

### Step 3: Nightly pipeline generates AAA.md

A nightly workflow (`tg aaa generate`) scans all open GitHub Issues for `folder:FOLDERNAME` labels and writes the issue body to `FOLDERNAME/AAA.md` on disk.

```
GitHub Issue #612 (labeled folder:TRUGS_COMPUTATION)
    │
    ▼  nightly tg aaa generate
    │
TRUGS_COMPUTATION/AAA.md  (read-only, auto-generated)
```

**Key rules:**
- One AAA.md per folder — if multiple issues have the same label, the most recent wins
- The `folder:` label maps to top-level directories only (no sub-folders)
- When an issue is closed, `AAA.md` is archived as `zzz_AAA_<title>.md`

### Step 4: Agent reads AAA.md and executes

The agent enters the folder, reads `folder.trug.json` (ground truth for structure) and `AAA.md` (ground truth for intent), and knows:

- What to build (VISION)
- Whether it's feasible (FEASIBILITY)
- Exact requirements (SPECIFICATIONS)
- System design (ARCHITECTURE)
- Task list and priorities (CODING)
- How to validate (TESTING)
- How to deploy (DEPLOYMENT)

The agent implements, updates `folder.trug.json`, creates a PR. **The agent never edits AAA.md.**

<trl>
AGENT claude SHALL READ FILE folder.trug.json THEN READ FILE AAA.md.
AGENT claude SHALL IMPLEMENT STRICTLY THE RECORD specification FROM FILE AAA.md.
AGENT claude SHALL WRITE RESULT TO FILE folder.trug.json AND FILE source.
AGENT claude SHALL_NOT WRITE TO FILE AAA.md.
AGENT claude SHALL DEFINE RESOURCE pull_request THEN SEND RESULT TO PARTY human THEN EXIT.
</trl>

```
Agent workflow:
1. Read folder.trug.json  → Understand structure
2. Read AAA.md            → Understand intent and tasks
3. Implement              → Write code, update tests
4. Update folder.trug.json → Reflect new/changed files
5. Create PR              → DONE
```

---

## Sub-Issues: Breaking Work Into Agent-Sized Pieces

Large issues are broken into sub-issues. There are two types:

### Type A — AAA Upgrade Sub-Issues

These improve the specification itself. The work is: edit the GitHub Issue body (not code).

Example: *"Phase 2 FEASIBILITY: Complete external research for PERAGO v2.0"*

After the edit, the nightly pipeline regenerates `AAA.md`. Type A sub-issues don't carry a `folder:` label themselves.

### Type B — Code Development Sub-Issues

These implement code specified in the parent issue. The work is: branch, code, PR.

Example: *"Implement CODING: widget endpoint per SPECIFICATIONS"*

### Sequencing rule

Type A (spec upgrade) should precede Type B (code development) for the same phase. Don't implement before the spec is written.

```
Sub-issue sequence:
1. "Phase 3 SPECIFICATIONS: Define API contract"  (Type A — spec)
2. "Implement CODING: widget endpoint"             (Type B — code)
3. "Phase 6 TESTING: Define acceptance tests"       (Type A — spec)
4. "Implement TESTING: run acceptance suite"         (Type B — code)
```

---

## What AAA.md Looks Like

A real AAA.md has all 9 phases, each with status and quality gate:

```markdown
## VISION
**Phase Status:** COMPLETE
**Quality Gate:** ✅

### What We're Building
User authentication service: SSO across 5 microservices.

### Why It Matters
- Current: separate logins per service (poor UX, security gaps)
- Target: <100ms p95 latency, zero password support tickets

### Success Criteria
- [ ] SSO works across all 5 services
- [ ] Auth latency < 100ms p95
- [ ] Zero password-related support tickets

---

## FEASIBILITY
**Phase Status:** COMPLETE
**Quality Gate:** ✅

### Research Bibliography
| # | Source | URL | Accessed | Relevance |
|---|--------|-----|----------|-----------|
| 1 | OAuth 2.1 Draft | https://... | 2026-03-01 | Core protocol |

### Assessment: MEDIUM
### Decision: GO

### Risks
| Risk | Severity | Mitigation | Source |
|------|----------|------------|--------|
| Token expiry race | Medium | Sliding window | Source #1 |

---

## SPECIFICATIONS
**Phase Status:** COMPLETE
**Quality Gate:** ✅

### Features & Acceptance Criteria
- [ ] POST /auth/login returns JWT within 100ms
- [ ] Token refresh via sliding window (no forced re-login)
...

---

## ARCHITECTURE
**Phase Status:** COMPLETE
**Quality Gate:** ✅

### Component Map
auth-service/ → JWT issuer, token validator, session store

### Tech Stack
| Layer | Tech | Justification |
|-------|------|---------------|
| Auth | OAuth 2.1 | Industry standard |

---

## VALIDATION
**Phase Status:** COMPLETE
**Quality Gate:** ✅

### HITM Validation Checks
- [x] Alignment: vision → specs → architecture consistent?
- [x] Completeness: enough detail to code?
- [x] Feasibility: technology choices verified?
- [x] Risk: risks identified and mitigated?
- [x] Scope: architecture delivers specs, no more no less?
- [x] Coding plan: files to create/modify, execution order, test strategy defined?

### Coding Plan
| Order | Action | File | Test |
|-------|--------|------|------|
| 1 | Create JWT issuer | auth-service/jwt.py | test_jwt.py |
| 2 | Create token validator middleware | auth-service/middleware.py | test_middleware.py |
| 3 | Integrate session store | auth-service/session.py | test_session.py |

**Human approved:** The plan covers all specification requirements. Execution order handles dependencies (issuer before validator). Test strategy: unit tests per module, integration test for full flow.

---

## CODING
**Phase Status:** IN_PROGRESS
**Quality Gate:** ⏳

### Tasks
- [x] JWT issuer implementation (HIGH)
- [ ] Token validator middleware (HIGH)
- [ ] Session store integration (MEDIUM)

---

## TESTING
**Phase Status:** NOT_STARTED
**Quality Gate:** ⏳

BLOCKED: Requires CODING complete

---

## DEPLOYMENT
**Phase Status:** NOT_APPLICABLE
**Quality Gate:** ✅

Library package — deployed via pip install.
```

### What the agent learns from this

Scanning this AAA.md, the agent knows in seconds:
- **Vision is done** — no need to question the goals
- **Feasibility is done** — GO decision, risks are documented
- **Specs are done** — exact acceptance criteria exist, no clarification needed
- **Architecture is done** — knows the components and tech stack
- **Coding is in progress** — JWT issuer done, two tasks remaining
- **Testing is blocked** — don't start testing yet
- **Deployment is N/A** — no deployment needed

The agent picks up where the last session left off: implement the token validator middleware. No onboarding conversation needed.

---

## The TRUG-Native Format (Optional)

For complex multi-component issues, the AAA can embed a **TRUG JSON graph** directly in the issue body. Each phase, task, risk, and dependency becomes a typed node with edges expressing relationships.

This is the `aaa_v1` vocabulary:

| Node Type | What It Represents |
|-----------|--------------------|
| `AAA` | Root node (one per issue) |
| `PHASE` | One of the 9 phases |
| `TASK` | Unit of work within a phase |
| `RISK` | Risk from FEASIBILITY |
| `ADR` | Architecture Decision Record |
| `DEPENDENCY` | External/internal dependency |
| `RESEARCH_SOURCE` | Bibliography entry |
| `QUALITY_GATE` | Validation gate between phases |
| `SUB_ISSUE` | Tracked sub-issue |

Edge relations include `precedes`, `depends_on`, `blocked_by`, `mitigates`, `validates`, `tracks`, `cites`, `decides`, `implements`.

The benefit: the nightly pipeline can validate the graph structure (all node IDs exist, edges point to real nodes, required properties present) *before* rendering `AAA.md`. Bad data is caught at write time, not at agent-execution time.

---

## Research Protocol: Why FEASIBILITY Requires Web Research

LLM training data has a cutoff. Technology versions change, libraries get deprecated, APIs evolve, pricing shifts. A feasibility study completed entirely from LLM memory is **incomplete by definition**.

Every FEASIBILITY phase must include:
1. **Web research** — verify every external technology assumption
2. **Research bibliography** — every claim cites a source with URL and access date
3. **Research gaps** — what couldn't be verified? These become tasks.

<trl>
STAGE feasibility SHALL REQUIRE DATA bibliography 'with EACH RECORD source CONTAINS STRING url AND STRING accessed.
AGENT claude SHALL VALIDATE EACH RECORD claim SUBJECT_TO DATA bibliography.
EACH RECORD claim 'that 'is INVALID SHALL REQUIRE A RECORD task TO VALIDATE.
AGENT claude SHALL_NOT APPROVE STAGE feasibility UNLESS ALL RECORD claim EQUALS VALID OR PENDING.
</trl>

Research depth scales with difficulty:
- **EASY:** 3+ sources
- **MEDIUM:** 5+ sources, including production case studies
- **HARD:** 8+ sources, including failure analysis
- **EXTREMELY_HARD:** 12+ sources, including academic papers

**Unverified claims must be flagged:**
```markdown
**Unverified Claims:**
- Redis 8.0 supports vector search natively — Source: LLM training data only. Requires verification.
```

---

## The Nightly Pipeline

The full nightly sequence (`.github/workflows/folder-sync.yml`, 07:00 UTC daily):

```
1. tg aaa generate     → Write AAA.md from GitHub Issues
2. tg sync      → Sync folder.trug.json stale flags
3. tg check     → Validate all TRUGs (continue on error)
4. tg render    → Regenerate all ARCHITECTURE.md
5. tg info       → Build root cross-folder graph
6. change_summary.py      → Generate change summary
7. git commit + push      → Commit all generated changes
8. Error issue (if any)   → Open issue for pipeline errors
```

**Manual trigger:**
```bash
tg aaa generate --root .
```

---

## Writing Style for AAA Issues

Since `AAA.md` is bounded by GitHub's ~65,536 character limit, every word costs:

- **Bullets over paragraphs** — scannable, not readable
- **Tables for comparisons** — risks, decisions, metrics, tech stack
- **Precise terms** — "10x cost savings" not "impressive savings"
- **Link, don't inline** — external detailed docs stay external
- **Target: <300 lines** for a typical issue body
- **Single line for blocked phases** — `BLOCKED: Requires X complete`

---

## Critical Rules for Agents

<trl>
RECORD issue GOVERNS FILE AAA.md.
AGENT claude SHALL READ FILE AAA.md THEN WRITE TO FILE folder.trug.json AND FILE source.
AGENT claude SHALL_NOT WRITE TO FILE AAA.md.
AGENT claude SHALL DEFINE RESOURCE pull_request THEN EXIT.
EACH RECORD issue SHALL CONTAIN ALL STAGE 'from STAGE vision TO STAGE deployment.
STAGE feasibility SHALL REQUIRE DATA bibliography FROM RESOURCE web.
AGENT claude SHALL_NOT IMPLEMENT STAGE coding UNLESS STAGE specifications EQUALS VALID.
AGENT claude SHALL MATCH STAGE 'that EQUALS FAILED THEN THROW ERROR THEN EXIT.
STAGE specifications PRODUCES DATA audit_checklist.
STAGE architecture PRODUCES DATA coding_plan.
STAGE audit CONTAINS DATA code_quality AND DATA plan_compliance.
STAGE audit SHALL VALIDATE DATA code_quality SUBJECT_TO DATA audit_checklist.
STAGE audit SHALL VALIDATE DATA plan_compliance SUBJECT_TO DATA coding_plan.
EACH RECORD deliverable FROM DATA coding_plan SHALL MATCH VALID OR STUB OR DEFERRED OR RECORD finding.
AGENT claude SHALL RETRY STAGE audit UNTIL ALL RECORD finding EQUALS VALID OR LOW.
EACH RECORD finding SHALL REQUIRE A RECORD test UNLESS RECORD finding EQUALS LOW.
</trl>

1. **GitHub Issues are source of truth.** AAA.md on disk is derived — never edit it.
2. **Read AAA.md, write to `folder.trug.json` and code.**
3. **Execution ends with: create PR.** Not "update AAA.md".
4. **All 9 phases always present** in every issue body.
5. **FEASIBILITY requires web research** — LLM training data alone is insufficient.
6. **Specs must be complete before coding** — if Phase 3 is `NOT_STARTED`, don't start Phase 5.
7. **When blocked: STOP.** Add to Blocked Tasks, report blockage, do not proceed.
8. **SPECIFICATIONS defines audit criteria.** Phase 3 outputs the audit checklist. Phase 8 executes against it.
9. **AUDIT writes tests.** Each finding that lacks coverage gets a test. Cycle until no critical/high.
10. **AUDIT checks plan compliance.** Every deliverable in the coding plan must be accounted for: `[DELIVERED]`, `[STUB]` (placeholder, future WP), `[DEFERRED]` (not built, moved to issue), or flagged as a finding. Code-only audits miss plan drift — a function can pass all tests but still be missing from the delivery.
11. **Plans use markers.** When a deliverable is intentionally incomplete, mark it `[STUB]` or `[DEFERRED]` with the reason and target issue. Unmarked unchecked items are findings.

---

## Summary: The Complete Flow

```
Human develops VISION_*, FEASIBILITY_*, SPEC_* docs on disk
    ↓
Human consolidates into GitHub Issue (9-phase AAA format)
    ↓
Nightly pipeline generates AAA.md in the folder
    ↓
Agent reads folder.trug.json + AAA.md
    ↓
Agent implements, updates TRUG, creates PR
    ↓
Human reviews PR, merges
    ↓
When issue closes: AAA.md archived as zzz_AAA_<title>.md
    ↓
Working docs either stay (permanent record) or get zzz_ archived
```

The entire system is designed so that an LLM agent, entering any folder for the first time, can go from zero context to productive implementation in three file reads: `folder.trug.json`, `AAA.md`, and one spec document. Everything else is either auto-generated (skip it), archived (ignore it), or clearly labeled by type (read only if needed).
