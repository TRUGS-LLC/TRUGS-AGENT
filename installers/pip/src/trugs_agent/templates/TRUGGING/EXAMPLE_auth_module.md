# Trugging Example: Auth Module

A walkthrough of the 4-level Trugging methodology applied to an authentication module.

---

## Level 1: System TRUG — `project.trug.json`

The auth module appears as one node in the system graph:

```json
{
  "id": "auth",
  "type": "MODULE",
  "properties": {"name": "Auth Module", "language": "python"},
  "parent_id": "api",
  "contains": [],
  "metric_level": "HECTO_MODULE",
  "dimension": "system"
}
```

Edges connect it to the rest of the system:

```json
{"from_id": "api", "to_id": "auth", "relation": "DEPENDS_ON"},
{"from_id": "auth", "to_id": "db", "relation": "READS"}
```

**What an LLM learns:** auth exists, the API depends on it, it reads from the database.

---

## Level 2: Component TRUG — `auth/folder.trug.json`

Inside the auth folder, each file and public interface is a node:

```json
{
  "nodes": [
    {"id": "handler", "type": "FILE", "properties": {"path": "handler.py", "purpose": "Request handlers — login, logout, token refresh"}, ...},
    {"id": "models", "type": "FILE", "properties": {"path": "models.py", "purpose": "User and Token data models"}, ...},
    {"id": "middleware", "type": "FILE", "properties": {"path": "middleware.py", "purpose": "Auth middleware — validates JWT on every request"}, ...},
    {"id": "UserService", "type": "SERVICE", "properties": {"name": "UserService"}, "parent_id": "handler", ...},
    {"id": "AuthMiddleware", "type": "FUNCTION", "properties": {"name": "AuthMiddleware"}, "parent_id": "middleware", ...}
  ],
  "edges": [
    {"from_id": "handler", "to_id": "models", "relation": "IMPORTS"},
    {"from_id": "middleware", "to_id": "models", "relation": "IMPORTS"},
    {"from_id": "UserService", "to_id": "AuthMiddleware", "relation": "DEPENDS_ON"}
  ]
}
```

**What an LLM learns:** three files, how they import each other, UserService depends on AuthMiddleware.

---

## Level 3: File Header TRUG/L — top of `auth/handler.py`

```python
# <trl>
# MODULE auth SHALL AUTHENTICATE ALL PARTY 'before GRANT ACCESS TO DATA.
# MODULE auth SHALL READ DATA credential FROM ENDPOINT environment_variable.
# MODULE auth SHALL_NOT WRITE DATA credential TO FILE OR STREAM log.
# MODULE auth SHALL VALIDATE DATA token SUBJECT_TO INTERFACE jwt_schema
#   THEN RETURN PARTY user OR THROW EXCEPTION auth_error.
# IF DATA token 'is EXPIRED THEN MODULE auth SHALL DENY PARTY
#   AND SEND ERROR TO PARTY caller.
# </trl>

import jwt
from config import SECRET_KEY
from models import User
```

**What an LLM learns:** 5 obligations and prohibitions — authenticate before access, read creds from env vars, never log secrets, validate tokens or throw, handle expiration. All in 5 sentences.

---

## Level 4: Inline TRUG/L — on `validate_token` function

```python
# <trl>FUNCTION validate_token SHALL VALIDATE DATA token SUBJECT_TO INTERFACE jwt_schema.
#   IF DATA token 'is INVALID OR EXPIRED THEN THROW EXCEPTION auth_error.
#   FUNCTION validate_token SHALL RETURN PARTY user 'with ACTIVE ACCESS.</trl>
def validate_token(token: str) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthError("Token expired")
    except jwt.InvalidTokenError:
        raise AuthError("Invalid token")
    return User.from_payload(payload)
```

**What an LLM learns:** this function's contract — validate JWT, throw on invalid/expired, return User. Can verify code matches, generate tests, detect drift.

---

## The Walkthrough

An LLM fixing a bug in auth reads 4 things:

1. `project.trug.json` → auth exists, API depends on it, it reads from DB
2. `auth/folder.trug.json` → handler.py, models.py, middleware.py, their imports
3. `auth/handler.py` header TRUG/L → module obligations: authenticate, never log secrets, handle expiration
4. Inline TRUG/L on `validate_token` → function contract: validate JWT, throw on expired, return User

System to function in 4 reads. No prose docs, no guessing, no asking.
