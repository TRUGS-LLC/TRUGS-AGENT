# AAA — Agent Instructions

<trl>
DEFINE "AAA" AS PIPELINE CONTAINS PHASE vision AND PHASE feasibility AND PHASE specifications AND PHASE architecture AND PHASE validation AND PHASE coding AND PHASE testing AND PHASE audit AND PHASE deployment.
DEFINE "PLANNING" AS STAGE CONTAINS PHASE vision AND PHASE feasibility AND PHASE specifications AND PHASE architecture AND PHASE validation.
DEFINE "EXECUTION" AS STAGE CONTAINS PHASE coding AND PHASE testing AND PHASE audit AND PHASE deployment.
PIPELINE AAA CONTAINS STAGE PLANNING AND STAGE EXECUTION.
</trl>

AAA is a 9-phase development protocol. Two cycles, three human touchpoints. This file teaches you every phase, every rule, every gate.

---

## Two Paths — No Middle Ground

<trl>
IF AGENT KNOWS ALL REQUIRED STEP THEN AGENT SHALL EXECUTE AS RECORD chore.
IF AGENT REQUIRES RECORD specification OR RECORD decision THEN AGENT SHALL CREATE RECORD issue THEN EXECUTE PHASE vision.
NO AGENT SHALL CREATE RECORD issue FOR RECORD chore.
NO AGENT SHALL SKIP STAGE PLANNING FOR RECORD issue.
</trl>

| Path | Trigger | Flow |
|------|---------|------|
| **CHORE** | You know exactly what to do | Branch → do it → PR → human merges |
| **ISSUE** | Something is unknown | Issue → AAA → PLANNING → HITM → EXECUTION → PR → human merges |

When in doubt, start as a chore. If unknowns emerge, upgrade to an issue.

---

## PLANNING Cycle (phases 1-5)

<trl>
PARTY human SHALL DEFINE PHASE vision.
AGENT SHALL EXECUTE PHASE feasibility THEN PHASE specifications THEN PHASE architecture.
PHASE specifications SHALL CONTAIN RECORD audit_criteria.
PHASE architecture SHALL CONTAIN RECORD coding_plan.
PARTY human SHALL APPROVE PHASE validation.
NO AGENT SHALL EXECUTE STAGE EXECUTION UNLESS PARTY human APPROVE PHASE validation.
</trl>

| # | Phase | Who | Output |
|---|-------|-----|--------|
| 1 | **VISION** | Human | Problem + success criteria |
| 2 | **FEASIBILITY** | Agent | GO/NO-GO + risks |
| 3 | **SPECIFICATIONS** | Agent | Requirements + **audit criteria for Phase 8** |
| 4 | **ARCHITECTURE** | Agent | Design + ADRs + **coding plan** |
| 5 | **VALIDATION** | **Human approves** | Plan is complete → proceed to coding |

**Phase 3 defines the audit. Phase 8 executes against it.** The plan defines what "done" looks like before any code is written.

### Phase 1: VISION

<trl>
PARTY human SHALL WRITE PHASE vision IN RECORD english.
PHASE vision SHALL CONTAIN RECORD problem AND RECORD success_criteria.
AGENT SHALL_NOT MODIFY PHASE vision.
AGENT SHALL READ PHASE vision THEN EXECUTE PHASE feasibility.
</trl>

The human states what they want in plain English. This is the only phase that does not use TRL — the human speaks naturally.

### Phase 2: FEASIBILITY

<trl>
AGENT SHALL ASSESS PHASE vision FOR RECORD technical_feasibility.
AGENT SHALL IDENTIFY ALL RECORD risk.
AGENT SHALL WRITE RECORD decision AS "GO" OR "NO-GO".
IF RECORD decision EQUALS "NO-GO" THEN AGENT SHALL WRITE RECORD alternative.
</trl>

Quick assessment. Can we build this? What are the risks? GO or NO-GO. If NO-GO, propose an alternative.

### Phase 3: SPECIFICATIONS

<trl>
AGENT SHALL WRITE ALL RECORD requirement SUBJECT_TO PHASE vision.
AGENT SHALL WRITE RECORD audit_criteria FOR PHASE audit.
EACH RECORD requirement SHALL BE WRITTEN AS RECORD trl_block.
EACH RECORD audit_criteria SHALL REFERENCE A RECORD requirement.
NO AGENT SHALL PROCEED TO PHASE architecture WITHOUT RECORD audit_criteria.
</trl>

Requirements in TRL. Every requirement gets audit criteria — specific, testable statements that Phase 8 will check against. If you can't write audit criteria for a requirement, the requirement isn't specific enough.

### Phase 4: ARCHITECTURE

<trl>
AGENT SHALL WRITE RECORD design SUBJECT_TO PHASE specifications.
AGENT SHALL WRITE RECORD coding_plan.
RECORD coding_plan SHALL CONTAIN RECORD file_list AND RECORD execution_order AND RECORD test_strategy.
AGENT MAY WRITE RECORD adr FOR EACH RECORD design_decision.
NO AGENT SHALL PROCEED TO PHASE validation WITHOUT RECORD coding_plan.
</trl>

System design plus a concrete coding plan. The coding plan lists files to create/modify, execution order, and test strategy. ADRs document non-obvious design decisions.

### Phase 5: VALIDATION (HITM Gate)

<trl>
AGENT SHALL VALIDATE PHASE specifications SUBJECT_TO PHASE vision.
AGENT SHALL VALIDATE PHASE architecture SUBJECT_TO PHASE specifications.
AGENT SHALL ASSERT PHASE specifications CONTAINS RECORD audit_criteria.
AGENT SHALL ASSERT PHASE architecture CONTAINS RECORD coding_plan.
AGENT SHALL ASSERT RECORD audit_criteria REFERENCES PHASE specifications.
NO AGENT SHALL PROCEED UNLESS ALL VALIDATION IS VALID.
PARTY human SHALL APPROVE PHASE validation BEFORE STAGE EXECUTION.
</trl>

Validation checks:
- **Alignment:** vision → specs → architecture consistent?
- **Completeness:** enough detail to code?
- **Feasibility:** technology choices verified?
- **Risk:** risks identified and mitigated?
- **Scope:** architecture delivers specs, no more no less?
- **Audit criteria:** defined in Phase 3, referencing specs?
- **Coding plan:** files, order, tests defined in Phase 4?

The agent runs these checks and presents results. The human approves before any coding begins.

---

## EXECUTION Cycle (phases 6-9)

<trl>
AGENT SHALL EXECUTE PHASE coding SUBJECT_TO RECORD coding_plan.
AGENT SHALL EXECUTE PHASE testing THEN PHASE audit.
PHASE audit SHALL VALIDATE RESULT SUBJECT_TO RECORD audit_criteria FROM PHASE specifications.
IF PHASE audit IS INVALID THEN AGENT SHALL FIX CODE THEN EXECUTE PHASE testing THEN EXECUTE PHASE audit.
EACH PHASE audit ROUND SHALL FIX ALL RECORD finding AND WRITE RECORD test FOR EACH RECORD finding.
NO AGENT SHALL EXECUTE PHASE deployment UNLESS PHASE audit IS VALID.
PARTY human SHALL APPROVE PHASE deployment.
</trl>

| # | Phase | Who | Output |
|---|-------|-----|--------|
| 6 | **CODING** | Agent | Working code per coding plan |
| 7 | **TESTING** | Agent | All tests pass |
| 8 | **AUDIT** | Agent + **Human approves** | Check against Phase 3 criteria. Cycles until clean. |
| 9 | **DEPLOYMENT** | Agent creates PR. **Human merges.** | Shipped |

### Phase 6: CODING

<trl>
AGENT SHALL IMPLEMENT CODE SUBJECT_TO RECORD coding_plan FROM PHASE architecture.
AGENT SHALL CREATE BRANCH BEFORE WRITE CODE.
AGENT SHALL FOLLOW RECORD execution_order FROM RECORD coding_plan.
AGENT SHALL_NOT ADD RECORD feature NOT IN PHASE specifications.
</trl>

Follow the coding plan. Don't add features that weren't specified. Don't improve code that wasn't in scope.

### Phase 7: TESTING

<trl>
AGENT SHALL WRITE RECORD test FOR EACH RECORD requirement FROM PHASE specifications.
AGENT SHALL EXECUTE ALL RECORD test.
IF RECORD test FAIL THEN AGENT SHALL FIX CODE THEN EXECUTE RECORD test.
NO AGENT SHALL PROCEED TO PHASE audit UNLESS ALL RECORD test PASS.
</trl>

Write tests that cover the specs. Run them. Fix failures. All tests must pass before audit.

### Phase 8: AUDIT (HITM Gate)

<trl>
AGENT SHALL CHECK EACH RECORD audit_criteria FROM PHASE specifications.
IF RECORD finding IS CRITICAL OR HIGH THEN AGENT SHALL FIX RECORD finding.
EACH RECORD fix SHALL INCLUDE RECORD test FOR RECORD finding.
AGENT SHALL EXECUTE PHASE testing AFTER EACH RECORD fix.
AGENT SHALL REPEAT PHASE audit UNTIL NO CRITICAL OR HIGH RECORD finding EXISTS.
PARTY human SHALL REVIEW PHASE audit RESULT.
</trl>

Check every audit criterion from Phase 3. For each finding: fix it AND write a test for it. Re-run the full test suite. Repeat until clean. The human reviews the final audit result.

### Phase 9: DEPLOYMENT

<trl>
AGENT SHALL CREATE RECORD pull_request WITH RECORD summary OF ALL PHASE.
AGENT SHALL RETURN RECORD url OF RECORD pull_request TO PARTY human.
AGENT SHALL STOP.
PARTY human SHALL MERGE RECORD pull_request.
NO AGENT SHALL MERGE RECORD pull_request.
</trl>

Create the PR. Return the URL. Stop. The human merges.

---

## Hard Rules

<trl>
NO AGENT SHALL COMMIT TO BRANCH main.
NO AGENT SHALL MERGE RECORD pull_request.
AGENT SHALL CREATE BRANCH THEN CREATE RECORD pull_request THEN STOP.
PARTY human SHALL MERGE RECORD pull_request.
NO AGENT SHALL EXECUTE PHASE coding UNLESS PHASE validation IS VALID.
NO AGENT SHALL EXECUTE PHASE deployment UNLESS PHASE audit IS VALID.
</trl>

These are not guidelines. They are prohibitions. Violating them is a system failure.

---

## AAA Document Format

An AAA document is a single markdown file with 9 sections, one per phase. Phase 1 is English. Phases 2-9 use TRL for specifications, criteria, and rules.

See [EXAMPLE_email_mcp.md](EXAMPLE_email_mcp.md) for a complete AAA from building an email MCP server — all 9 phases, TRL specs, audit criteria, and coding plan.
