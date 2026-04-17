# Security Policy

## Reporting a vulnerability

**Do not open a public issue for security problems.** Instead, report privately via GitHub's security advisory workflow:

1. Go to [github.com/TRUGS-LLC/TRUGS-AGENT/security/advisories/new](https://github.com/TRUGS-LLC/TRUGS-AGENT/security/advisories/new)
2. Fill in the details: the bug, its impact, how to reproduce it
3. We'll respond within 5 business days

If you cannot use GitHub Security Advisories, email `xepayac@gmail.com` with `[TRUGS-AGENT SECURITY]` in the subject line.

## What counts as a security issue

TRUGS-AGENT ships agent-instruction templates and thin installers. Security issues most likely surface in:

- The `installers/npm/` and `installers/pip/` packages — arbitrary file write, path traversal, or code execution during `create-trugs-agent` / `trugs-agent-init`
- Vendored `tools/validate.py` if crafted input causes resource exhaustion or arbitrary read (upstream TRUGS — we'll forward)
- A template file that, if followed literally by an LLM, steers it into dangerous behavior (prompt injection exposure)

Bugs that are **not** security issues (just file a normal issue):
- An installer fails on a specific OS or Node/Python version
- A template doesn't produce the behavior you expected from your LLM
- A broken link or typo in an agent instruction file

## Supported versions

TRUGS-AGENT tracks its own SemVer line, published on npm (`create-trugs-agent`) and PyPI (`trugs-agent`). Only the latest minor receives security fixes.

| Version | Supported |
|---------|-----------|
| Latest on npm + PyPI | Yes |
| Prior versions | No — upgrade |

## Our commitment

- Acknowledge receipt within 5 business days
- Keep you informed during investigation
- Credit you in the advisory and CHANGELOG (unless you prefer anonymity)
- Publish a fix within 30 days for high/critical findings, or explain why more time is needed

## Scope

This policy covers `TRUGS-LLC/TRUGS-AGENT` — the instruction templates, installers, and documentation in this repository. For the underlying TRUGS specification and reference tools, see `TRUGS-LLC/TRUGS/SECURITY.md`.
