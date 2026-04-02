# Trugging — Agent Instructions

<trl>
DEFINE "Trugging" AS PIPELINE CONTAINS STAGE system AND STAGE component AND STAGE file_header AND STAGE inline.
STAGE system SHALL PRODUCE DATA graph AS FILE project.trug.json.
STAGE component SHALL PRODUCE DATA graph AS FILE folder.trug.json.
STAGE file_header SHALL PRODUCE RECORD trl_block AT ENTRY FILE.
STAGE inline SHALL PRODUCE RECORD trl_block AT ENTRY FUNCTION.
EACH STAGE SHALL EXECUTE SEQUENTIAL FROM STAGE system TO STAGE inline.
</trl>

Trugging is how you describe a program using TRUGs and TRL. Four levels, top-down. Graphs for structure, sentences for behavior.

---

## Level 1: System — `project.trug.json`

<trl>
AGENT SHALL CREATE FILE project.trug.json AT ENTRY NAMESPACE project.
EACH SERVICE SHALL BE A DATA node IN FILE project.trug.json.
EACH STREAM SHALL BE A DATA node IN FILE project.trug.json.
EACH MODULE SHALL BE A DATA node IF MODULE IS ENTRY OR EXIT.
EACH DATA node SHALL CONTAIN RECORD name AND RECORD type AND RECORD dimension.
AGENT SHALL CREATE DATA edge FOR EACH RECORD dependency BETWEEN DATA node.
AGENT SHALL_NOT CREATE DATA node FOR RECORD implementation_detail.
</trl>

### What Goes In

Nodes: services, databases, message queues, external APIs, top-level modules. Things that exist independently and have names a human would recognize.

Edges: `DEPENDS_ON`, `READS`, `WRITES`, `FEEDS`, `AUTHENTICATES`, `IMPLEMENTS`. How the big pieces connect.

### What Stays Out

Internal classes, helper functions, utility files. If it doesn't appear in an architecture diagram, it doesn't appear in the system TRUG.

### Example

```json
{
  "name": "My App",
  "version": "1.0.0",
  "type": "SYSTEM",
  "dimensions": {
    "system": {"description": "System architecture", "base_level": "BASE"}
  },
  "capabilities": {"extensions": [], "vocabularies": ["core_v1.0.0"], "profiles": []},
  "nodes": [
    {"id": "api", "type": "SERVICE", "properties": {"name": "API Server", "language": "python"}, "parent_id": null, "contains": ["auth", "handlers"], "metric_level": "KILO_SERVICE", "dimension": "system"},
    {"id": "auth", "type": "MODULE", "properties": {"name": "Auth Module"}, "parent_id": "api", "contains": [], "metric_level": "HECTO_MODULE", "dimension": "system"},
    {"id": "handlers", "type": "MODULE", "properties": {"name": "Request Handlers"}, "parent_id": "api", "contains": [], "metric_level": "HECTO_MODULE", "dimension": "system"},
    {"id": "db", "type": "STREAM", "properties": {"name": "PostgreSQL", "engine": "postgres"}, "parent_id": null, "contains": [], "metric_level": "KILO_STREAM", "dimension": "system"},
    {"id": "queue", "type": "STREAM", "properties": {"name": "Task Queue", "engine": "redis"}, "parent_id": null, "contains": [], "metric_level": "KILO_STREAM", "dimension": "system"}
  ],
  "edges": [
    {"from_id": "api", "to_id": "db", "relation": "READS"},
    {"from_id": "api", "to_id": "db", "relation": "WRITES"},
    {"from_id": "api", "to_id": "queue", "relation": "WRITES"},
    {"from_id": "api", "to_id": "auth", "relation": "DEPENDS_ON"},
    {"from_id": "handlers", "to_id": "auth", "relation": "DEPENDS_ON"}
  ]
}
```

---

## Level 2: Component — `folder.trug.json`

<trl>
AGENT SHALL CREATE FILE folder.trug.json AT ENTRY EACH MODULE.
EACH FILE IN MODULE SHALL BE A DATA node.
EACH SERVICE OR FUNCTION THAT IS PUBLIC SHALL BE A DATA node.
AGENT SHALL CREATE DATA edge FOR EACH RECORD import BETWEEN FILE.
AGENT SHALL CREATE DATA edge FOR EACH RECORD call BETWEEN SERVICE OR FUNCTION.
AGENT SHALL_NOT CREATE DATA node FOR PRIVATE FUNCTION UNLESS FUNCTION IS CRITICAL.
</trl>

### What Goes In

Nodes: every file in the folder, plus public classes/services/interfaces that other modules depend on.

Edges: `IMPORTS`, `CALLS`, `IMPLEMENTS`, `EXTENDS`, `CONTAINS`. How the files and their exports relate.

### What Stays Out

Private helper functions, internal constants, implementation details that don't cross a file boundary.

### Example

```json
{
  "name": "Auth Module",
  "version": "1.0.0",
  "type": "MODULE",
  "dimensions": {
    "code": {"description": "Code structure", "base_level": "BASE"}
  },
  "capabilities": {"extensions": [], "vocabularies": ["core_v1.0.0"], "profiles": []},
  "nodes": [
    {"id": "handler", "type": "FILE", "properties": {"path": "handler.py"}, "parent_id": null, "contains": ["UserService"], "metric_level": "DEKA_FILE", "dimension": "code"},
    {"id": "models", "type": "FILE", "properties": {"path": "models.py"}, "parent_id": null, "contains": ["User", "Token"], "metric_level": "DEKA_FILE", "dimension": "code"},
    {"id": "middleware", "type": "FILE", "properties": {"path": "middleware.py"}, "parent_id": null, "contains": ["AuthMiddleware"], "metric_level": "DEKA_FILE", "dimension": "code"},
    {"id": "UserService", "type": "SERVICE", "properties": {"name": "UserService"}, "parent_id": "handler", "contains": [], "metric_level": "BASE_SERVICE", "dimension": "code"},
    {"id": "User", "type": "RECORD", "properties": {"name": "User"}, "parent_id": "models", "contains": [], "metric_level": "BASE_RECORD", "dimension": "code"},
    {"id": "Token", "type": "RECORD", "properties": {"name": "Token"}, "parent_id": "models", "contains": [], "metric_level": "BASE_RECORD", "dimension": "code"},
    {"id": "AuthMiddleware", "type": "FUNCTION", "properties": {"name": "AuthMiddleware"}, "parent_id": "middleware", "contains": [], "metric_level": "BASE_FUNCTION", "dimension": "code"}
  ],
  "edges": [
    {"from_id": "handler", "to_id": "models", "relation": "IMPORTS"},
    {"from_id": "middleware", "to_id": "models", "relation": "IMPORTS"},
    {"from_id": "UserService", "to_id": "User", "relation": "READS"},
    {"from_id": "UserService", "to_id": "Token", "relation": "VALIDATES"},
    {"from_id": "AuthMiddleware", "to_id": "Token", "relation": "VALIDATES"}
  ]
}
```

---

## Level 3: File Header — `<trl>` block

<trl>
AGENT SHALL WRITE RECORD trl_block AT ENTRY EACH FILE THAT CONTAINS PUBLIC FUNCTION OR SERVICE.
RECORD trl_block SHALL DESCRIBE ALL RECORD obligation FOR MODULE.
RECORD trl_block SHALL DESCRIBE ALL RECORD prohibition FOR MODULE.
RECORD trl_block SHALL DESCRIBE ALL RECORD interface THAT MODULE IMPLEMENTS OR DEPENDS_ON.
AGENT SHALL_NOT DESCRIBE RECORD implementation_detail IN RECORD trl_block.
EACH RECORD trl_block SHALL CONTAIN 3 TO 8 RECORD sentence.
</trl>

### What Goes In

Obligations (SHALL), prohibitions (SHALL_NOT), interfaces, error handling contracts. What the module promises to do and promises not to do.

### What Stays Out

How it works internally. The header describes the *contract*, not the *mechanism*. An agent reads the header to know what the module guarantees — not how it achieves those guarantees.

### How to Write It

<trl>
AGENT SHALL IDENTIFY ALL PUBLIC FUNCTION IN FILE.
AGENT SHALL IDENTIFY ALL RECORD obligation — WHAT MUST FILE DO.
AGENT SHALL IDENTIFY ALL RECORD prohibition — WHAT MUST FILE NOT DO.
AGENT SHALL IDENTIFY ALL RECORD interface — WHAT DOES FILE DEPEND ON OR EXPOSE.
AGENT SHALL IDENTIFY ALL RECORD exception — WHAT CAN GO WRONG.
AGENT SHALL WRITE EACH AS RECORD sentence IN RECORD trl_block.
</trl>

### Example

```python
# <trl>
# MODULE auth SHALL AUTHENTICATE ALL PARTY BEFORE GRANT ACCESS TO DATA.
# MODULE auth SHALL READ DATA credential FROM ENDPOINT environment_variable.
# MODULE auth SHALL_NOT WRITE DATA credential TO FILE OR STREAM log.
# MODULE auth SHALL VALIDATE DATA token SUBJECT_TO INTERFACE jwt_schema
#   THEN RETURN PARTY user OR THROW EXCEPTION auth_error.
# IF DATA token IS EXPIRED THEN MODULE auth SHALL DENY PARTY
#   AND SEND ERROR TO PARTY caller.
# </trl>

import jwt
from config import SECRET_KEY
...
```

---

## Level 4: Inline — `<trl>` in code comments

<trl>
AGENT SHALL WRITE RECORD trl_block BEFORE EACH FUNCTION THAT IS PUBLIC OR CRITICAL.
AGENT MAY WRITE RECORD trl_block BEFORE RECORD code_block THAT IS COMPLEX.
EACH INLINE RECORD trl_block SHALL CONTAIN 1 TO 3 RECORD sentence.
RECORD trl_block SHALL DESCRIBE RECORD contract — INPUT AND OUTPUT AND EXCEPTION.
AGENT SHALL_NOT WRITE RECORD trl_block FOR TRIVIAL FUNCTION.
</trl>

### What Goes In

Function contracts: what it takes, what it returns, what it throws, and any non-obvious obligation. One to three sentences.

### What Stays Out

Trivial functions. A getter, a simple constructor, a one-line utility — these don't need TRL. If the function signature tells the whole story, don't repeat it in TRL.

### When to Write Inline TRL

<trl>
AGENT SHALL WRITE INLINE RECORD trl_block IF FUNCTION IS PUBLIC.
AGENT SHALL WRITE INLINE RECORD trl_block IF FUNCTION CONTAINS RECORD side_effect.
AGENT SHALL WRITE INLINE RECORD trl_block IF FUNCTION CONTAINS RECORD security OBLIGATION.
AGENT SHALL WRITE INLINE RECORD trl_block IF FUNCTION CONTAINS RECORD retry OR RECORD timeout.
AGENT MAY SKIP INLINE RECORD trl_block IF FUNCTION IS PRIVATE AND TRIVIAL.
</trl>

### Example

```python
# <trl>FUNCTION validate_token SHALL VALIDATE DATA token SUBJECT_TO INTERFACE jwt_schema.
#   IF DATA token IS INVALID OR EXPIRED THEN THROW EXCEPTION auth_error.
#   FUNCTION validate_token SHALL RETURN PARTY user WITH ACTIVE ACCESS.</trl>
def validate_token(token: str) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthError("Token expired")
    except jwt.InvalidTokenError:
        raise AuthError("Invalid token")
    return User.from_payload(payload)


# <trl>FUNCTION send_welcome SHALL SEND MESSAGE welcome TO PARTY user
#   THEN WRITE RECORD log. FUNCTION send_welcome SHALL RETRY BOUNDED 3.</trl>
def send_welcome(user: User):
    for attempt in range(3):
        try:
            email.send(user.email, WELCOME_TEMPLATE)
            logger.info(f"Welcome sent to {user.id}")
            return
        except SMTPError:
            if attempt == 2:
                raise
```

---

## The Boundary Rule

<trl>
DEFINE "boundary" AS ENTRY FILE.
IF RECORD description IS ABOVE ENTRY FILE THEN AGENT SHALL USE DATA graph.
IF RECORD description IS BELOW ENTRY FILE THEN AGENT SHALL USE RECORD trl_block.
DATA graph SHALL DESCRIBE RECORD structure — WHAT EXISTS AND HOW IT CONNECTS.
RECORD trl_block SHALL DESCRIBE RECORD behavior — WHAT MUST HAPPEN AND WHAT MUST NOT.
</trl>

| Level | Format | Describes | Agent Question |
|-------|--------|-----------|----------------|
| System | TRUG graph | Services, databases, top-level modules | What exists? |
| Component | TRUG graph | Files, classes, public interfaces | What's inside this module? |
| File header | TRL sentences | Module obligations and prohibitions | What are the contracts? |
| Inline | TRL sentences | Function contracts and side effects | What does this function guarantee? |

**Above the file: graph. Inside the file: sentences.**

---

## Trugging a Codebase — Step by Step

<trl>
AGENT SHALL EXECUTE STAGE system THEN STAGE component THEN STAGE file_header THEN STAGE inline.
AGENT SHALL_NOT EXECUTE STAGE inline BEFORE STAGE system.
EACH STAGE SHALL COMPLETE BEFORE NEXT STAGE BEGINS.
</trl>

### Step 1: System TRUG

<trl>
AGENT SHALL READ ALL FILE IN NAMESPACE project AT DEPTH 1.
AGENT SHALL IDENTIFY ALL SERVICE AND STREAM AND MODULE.
AGENT SHALL CREATE FILE project.trug.json WITH ALL DATA node AND DATA edge.
AGENT SHALL VALIDATE FILE project.trug.json.
</trl>

Scan the project root. Identify the big pieces. Create `project.trug.json`. Validate.

### Step 2: Component TRUGs

<trl>
AGENT SHALL READ EACH MODULE IDENTIFIED IN STAGE system.
FOR EACH MODULE AGENT SHALL CREATE FILE folder.trug.json.
AGENT SHALL VALIDATE EACH FILE folder.trug.json.
</trl>

For each major folder, create a `folder.trug.json`. Map files, public interfaces, imports, calls. Validate.

### Step 3: File Headers

<trl>
AGENT SHALL READ EACH FILE THAT CONTAINS PUBLIC FUNCTION OR SERVICE.
FOR EACH FILE AGENT SHALL WRITE RECORD trl_block AT ENTRY FILE.
AGENT SHALL ASSERT RECORD trl_block CONTAINS RECORD obligation OR RECORD prohibition.
</trl>

For each non-trivial file, write a `<trl>` header. Cover obligations, prohibitions, interfaces, error contracts.

### Step 4: Inline TRL

<trl>
AGENT SHALL READ EACH PUBLIC FUNCTION AND EACH CRITICAL FUNCTION.
FOR EACH FUNCTION AGENT SHALL WRITE INLINE RECORD trl_block.
AGENT MAY SKIP TRIVIAL FUNCTION.
</trl>

For each public or critical function, write an inline `<trl>` comment. Cover inputs, outputs, exceptions, side effects.

---

## Maintaining TRUGs

<trl>
IF AGENT CREATE FILE THEN AGENT SHALL UPDATE FILE folder.trug.json.
IF AGENT DELETE FILE THEN AGENT SHALL UPDATE FILE folder.trug.json.
IF AGENT CREATE SERVICE OR MODULE THEN AGENT SHALL UPDATE FILE project.trug.json.
IF AGENT MODIFY RECORD contract OF FUNCTION THEN AGENT SHALL UPDATE INLINE RECORD trl_block.
AGENT SHALL_NOT MODIFY RECORD trl_block WITHOUT MODIFYING RECORD code OR RECORD code WITHOUT MODIFYING RECORD trl_block.
</trl>

TRUGs and TRL stay in sync with code. When code changes, the description changes. When the description changes, the code changes. Drift between the two is a bug.
