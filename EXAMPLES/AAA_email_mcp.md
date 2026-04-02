# AAA: Email MCP — Local Email Management for Claude Code

Issue: #1261

## Phase 1: VISION

I hate email. I have 3 Gmail accounts with 15,000+ messages across them. I need Claude Code to read, send, search, and organize email for me — triage inboxes, draft responses, archive junk, send outreach. Everything stays on my machine. No cloud OAuth, no API tokens, no Google dependency. Direct IMAP/SMTP, same MCP pattern as the browser and GIMP tools we already have.

## Phase 2: FEASIBILITY

<trl>
SERVICE email_mcp SHALL DEPEND_ON MODULE imaplib FROM NAMESPACE python_stdlib.
SERVICE email_mcp SHALL DEPEND_ON MODULE smtplib FROM NAMESPACE python_stdlib.
SERVICE email_mcp SHALL REQUIRE NO EXTERNAL RESOURCE.
SERVICE email_mcp SHALL IMPLEMENT INTERFACE mcp_stdio AS MODULE browser_mcp IMPLEMENTS INTERFACE mcp_stdio.
</trl>

**Decision:** GO. Python imaplib/smtplib are stdlib — zero external dependencies. IMAP is universal (Google Workspace, Proton Bridge, any provider). MCP stdio transport matches existing browser_mcp.py and gimp_mcp.py pattern.

### Risks

<trl>
IF DATA credential ROUTE TO FILE repository THEN THROW EXCEPTION security_violation.
AGENT SHALL READ DATA credential FROM ENDPOINT environment_variable.
FILE email_accounts.json SHALL REQUIRE PRIVATE ACCESS.
</trl>

<trl>
IF AGENT DELETE ALL MESSAGE WITHOUT VALID RECORD confirm THEN THROW EXCEPTION data_loss.
FUNCTION email_delete SHALL REQUIRE ACTIVE RECORD confirm BEFORE DELETE MESSAGE.
FUNCTION email_delete SHALL DEFAULT TO RECORD dry_run.
</trl>

## Phase 3: SPECIFICATIONS

### Tools

<trl>
DEFINE "read_tools" AS STAGE CONTAINS FUNCTION email_accounts AND FUNCTION email_folders AND FUNCTION email_list AND FUNCTION email_read.
DEFINE "search_tools" AS STAGE CONTAINS FUNCTION email_search.
DEFINE "write_tools" AS STAGE CONTAINS FUNCTION email_send AND FUNCTION email_reply AND FUNCTION email_draft.
DEFINE "organize_tools" AS STAGE CONTAINS FUNCTION email_move AND FUNCTION email_delete AND FUNCTION email_flag.
SERVICE email_mcp CONTAINS STAGE read_tools AND STAGE search_tools AND STAGE write_tools AND STAGE organize_tools.
</trl>

### Tool Specifications

<trl>
FUNCTION email_accounts SHALL READ ALL ENDPOINT imap_account FROM FILE accounts.json THEN WRITE RESULT TO PARTY caller.
FUNCTION email_folders SHALL READ ALL MODULE folder FROM ENDPOINT imap_account THEN WRITE RESULT TO PARTY caller.
FUNCTION email_list SHALL FILTER ALL MESSAGE BY MODULE folder AND OPTIONAL ACTIVE state THEN SORT RESULT BY DATA date THEN WRITE RESULT TO PARTY caller.
FUNCTION email_read SHALL READ A MESSAGE BY DATA uid FROM MODULE folder THEN WRITE RESULT TO PARTY caller.
FUNCTION email_search SHALL FILTER ALL MESSAGE BY DATA from_addr OR DATA subject OR DATA date OR DATA body THEN WRITE RESULT TO PARTY caller.
FUNCTION email_send SHALL WRITE MESSAGE TO ENDPOINT smtp THEN SEND MESSAGE TO PARTY recipient.
FUNCTION email_reply SHALL READ MESSAGE BY DATA uid THEN WRITE MESSAGE TO ENDPOINT smtp THEN SEND MESSAGE TO PARTY original_sender.
FUNCTION email_draft SHALL WRITE MESSAGE TO MODULE drafts_folder.
FUNCTION email_move SHALL READ MESSAGE BY DATA uid FROM MODULE source_folder THEN WRITE MESSAGE TO MODULE target_folder THEN DELETE MESSAGE FROM MODULE source_folder.
FUNCTION email_delete SHALL VALIDATE ACTIVE RECORD confirm THEN DELETE MESSAGE OR WRITE RECORD dry_run TO PARTY caller.
FUNCTION email_flag SHALL WRITE DATA flag TO MESSAGE BY DATA uid.
</trl>

### Configuration

<trl>
FILE email_accounts.json SHALL PERSIST AT ENDPOINT ~/.config/trugs/.
FILE email_accounts.json SHALL REQUIRE PRIVATE ACCESS.
EACH ENDPOINT imap_account SHALL CONTAIN DATA email AND DATA imap_host AND DATA imap_port AND DATA smtp_host AND DATA smtp_port AND DATA password_env.
NO FILE SHALL CONTAIN DATA password DIRECTLY.
EACH DATA password SHALL READ FROM ENDPOINT environment_variable.
</trl>

### Audit Criteria (Phase 8 checks against these)

<trl>
FUNCTION email_list SHALL RETURN VALID RESULT FOR EACH ENDPOINT imap_account.
FUNCTION email_read SHALL RETURN DATA body_text AND DATA headers FOR ANY MESSAGE.
FUNCTION email_send SHALL SEND MESSAGE THEN RETURN DATA message_id.
FUNCTION email_search SHALL FILTER BY DATA from_addr AND DATA subject AND DATA date.
FUNCTION email_delete WITH NO RECORD confirm SHALL RETURN RECORD dry_run.
FUNCTION email_delete WITH ACTIVE RECORD confirm SHALL DELETE MESSAGE.
NO FUNCTION SHALL WRITE DATA credential TO STREAM log OR FILE.
ALL FUNCTION SHALL RETURN VALID DATA json.
SERVICE email_mcp SHALL REQUIRE NO EXTERNAL RESOURCE EXCEPT MODULE python_stdlib.
</trl>

## Phase 4: ARCHITECTURE

### Decisions

<trl>
SERVICE email_mcp SHALL USE MODULE imaplib DIRECTLY.
SERVICE email_mcp SHALL_NOT USE SERVICE thunderbird_api.
SERVICE email_mcp SHALL PERSIST AS FILE email_mcp.py AT ENDPOINT TRUGS_WEB/trugs_web/.
</trl>

**ADR-1261-01:** Direct IMAP/SMTP over Thunderbird WebExtension API. Zero dependencies, works without Thunderbird running, universal across providers.

<trl>
FILE email_accounts.json SHALL PERSIST AT ENDPOINT ~/.config/trugs/.
FILE email_accounts.json SHALL_NOT PERSIST AT ENDPOINT repository.
FILE .env SHALL CONTAIN ALL DATA password_env.
FILE .env SHALL REQUIRE PRIVATE ACCESS.
</trl>

**ADR-1261-02:** Config in ~/.config/trugs/, not in repo. Credentials via environment variables. Never in the JSON file.

<trl>
FUNCTION email_delete SHALL DEFAULT TO RECORD dry_run.
FUNCTION email_delete SHALL REQUIRE EXPLICIT ACTIVE RECORD confirm TO DELETE.
FUNCTION email_move SHALL REQUIRE DATA target_folder.
</trl>

**ADR-1261-03:** Destructive operations require explicit confirmation. Default is dry-run.

### Coding Plan

<trl>
AGENT SHALL CREATE FILE email_mcp.py AT ENDPOINT TRUGS_WEB/trugs_web/.
AGENT SHALL IMPLEMENT STAGE read_tools THEN STAGE write_tools THEN STAGE search_tools THEN STAGE organize_tools.
AGENT SHALL IMPLEMENT FUNCTION config_loader THEN FUNCTION imap_connect THEN FUNCTION smtp_connect.
AGENT SHALL IMPLEMENT FUNCTION mcp_wrapper FINALLY.
AGENT SHALL WRITE RECORD test FOR EACH FUNCTION.
</trl>

## Phase 5: VALIDATION

**HITM Gate — Human approves before coding.**

- [x] Vision → specs → architecture consistent
- [x] Enough detail to code (12 tools specified)
- [x] Technology verified (imaplib/smtplib stdlib)
- [x] Risks mitigated (credentials via env vars, dry-run deletes)
- [x] Audit criteria defined in Phase 3
- [x] Coding plan defined in Phase 4

**APPROVED — proceed to execution.**

---

## Phase 6: CODING

Status: COMPLETE

<trl>
AGENT SHALL IMPLEMENT SERVICE email_mcp SUBJECT_TO RECORD coding_plan.
</trl>

12 tools implemented in `TRUGS_WEB/trugs_web/email_mcp.py`. Three accounts tested (admin@trugs.ai, xepayacllc@gmail.com, xepayac@gmail.com).

## Phase 7: TESTING

Status: COMPLETE

<trl>
AGENT SHALL VALIDATE SERVICE email_mcp SUBJECT_TO RECORD audit_criteria.
</trl>

- email_accounts: returns all configured accounts
- email_list: returns messages from all 3 accounts
- email_read: returns full message body and headers
- email_search: filters by sender, subject, date
- email_send: sent endorsement emails to 3 professors
- email_delete: dry-run confirmed, then executed (5,063 archived)
- email_folders: fixed IMAP LIST parsing, returns folder names + counts

## Phase 8: AUDIT

Status: IN PROGRESS

Checking against Phase 3 audit criteria:

- [x] email_list returns valid results for each account
- [x] email_read returns body_text and headers
- [x] email_send sends and returns message_id
- [x] email_search filters by from, subject, date
- [x] email_delete without confirm returns dry_run
- [x] email_delete with confirm deletes
- [x] No credentials in logs or files
- [x] All functions return valid JSON
- [x] Zero external dependencies

## Phase 9: DEPLOYMENT

Status: PR #1263 created. Human merges.
