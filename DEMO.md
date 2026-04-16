# Before & After: TRUGS Agent

## Before — English Instructions

Your `CLAUDE.md` says:

```markdown
Please make sure to validate all inputs before saving to the database.
Always write tests for new functions.
Don't commit directly to main.
Keep the code clean and well-documented.
```

**What happens:**
- "Validate inputs" — sometimes checks types, sometimes checks values, sometimes does nothing
- "Always write tests" — skips tests when it seems like a small change
- "Don't commit to main" — follows it today, forgets it tomorrow
- "Keep the code clean" — subjective, different every run

**Result:** Inconsistent behavior. You re-explain the same rules every session.

---

## After — TRUG/L Instructions

Your `CLAUDE.md` says:

```markdown
<trl>
AGENT SHALL VALIDATE ALL REQUIRED RECORD SUBJECT_TO INTERFACE schema.
AGENT SHALL REQUIRE RECORD test FOR EACH FUNCTION.
AGENT SHALL_NOT WRITE ANY DATA TO ENDPOINT main.
AGENT SHALL CREATE RESOURCE branch THEN WRITE ALL DATA TO RESOURCE branch.
</trl>
```

**What happens:**
- `SHALL VALIDATE` — obligation, not suggestion. Failure is a violation.
- `REQUIRE RECORD test FOR EACH FUNCTION` — explicit scope, no wiggle room.
- `SHALL_NOT WRITE ... TO ENDPOINT main` — hard prohibition with defined semantics.
- `SHALL CREATE RESOURCE branch THEN WRITE` — exact sequence of operations.

**Result:** Same behavior every time. Every instruction has one meaning. The graph is auditable.

---

## Side-by-Side: Specifying an API

### English (ambiguous)

```
Build an authentication endpoint. It should validate the user's credentials,
return a token if valid, and handle errors gracefully.
```

- "Should" — is this required or optional?
- "Handle errors gracefully" — what does "gracefully" mean?
- "Return a token" — what kind? Where? To whom?

### TRUG/L (exact)

```
<trl>
SERVICE auth SHALL AUTHENTICATE PARTY user
  THEN READ DATA credentials FROM STREAM database
  THEN VALIDATE DATA credentials SUBJECT_TO INTERFACE auth_schema.
IF DATA credentials EQUALS VALID
  THEN SERVICE auth SHALL WRITE RECORD token TO PARTY user.
IF DATA credentials EQUALS INVALID
  THEN SERVICE auth SHALL SEND ERROR TO PARTY user.
SERVICE auth SHALL RESPOND WITHIN 200ms.
</trl>
```

- `SHALL AUTHENTICATE` — required obligation on a named service
- `SUBJECT_TO INTERFACE auth_schema` — explicit validation target
- `IF ... EQUALS VALID THEN ... WRITE RECORD token TO PARTY user` — exact conditional with named output and destination
- `IF ... EQUALS INVALID THEN ... SEND ERROR` — explicit error path, not "graceful handling"
- `SHALL RESPOND WITHIN 200ms` — measurable performance constraint

Every word compiles to a graph node or edge. The LLM executes the graph, not a vague interpretation.

---

## Try It Yourself

```bash
# Copy AGENT.md into your project
curl -o CLAUDE.md https://raw.githubusercontent.com/TRUGS-LLC/TRUGS-AGENT/main/AGENT.md

# Open your IDE and ask your LLM:
# "Read CLAUDE.md and write a TRUG/L specification for [your module]"
```

See [examples/](examples/) for a complete working project.
