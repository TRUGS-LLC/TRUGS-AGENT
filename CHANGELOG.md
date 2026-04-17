# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-04-18

Polish release — all three Dark Code compliance layers PASS for `TRUGS-LLC/TRUGS-AGENT`.

### Added
- `.github/workflows/compliance.yml` — CI gate validating `folder.trug.json` on every PR (#32)
- `SECURITY.md` — private disclosure via GitHub Security Advisories (#32)
- `.github/ISSUE_TEMPLATE/` — `bug_report.yml` + `feature_request.yml` + `config.yml` (#32)
- `.github/PULL_REQUEST_TEMPLATE.md` — summary, linked issue, compliance checklist (#32)
- `CHANGELOG.md` — this file, initialized retroactively after v1.1.0 (#33)
- README mermaid architecture diagram above-the-fold showing the LLM ↔ AGENT.md ↔ TRUG/L ↔ TRUG graph ↔ validator loop (#34)
- README "This repo, as a TRUG" section with three copy-paste queries against `folder.trug.json` (#34)

### Changed
- `folder.trug.json` — 57 errors + 6 warnings → 0 / 0 (#31). Edge relations aligned to folder-branch vocabulary, invalid `DATA` node types fixed, missing `contains` edges added, `name`/filename alignment for 6 nodes.
- `installers/pip/src/trugs_agent/cli.py` — added `<trl>` preamble on `main()` for Dark Code compliance (#33)
- `installers/pip/pyproject.toml` — version 1.1.0 → 1.2.0 (this release)
- `installers/npm/package.json` — version 1.0.0 → 1.2.0 (this release; synchronizes with pip)

### Release discipline
- Retroactive GitHub Release cut for this version (the first one; 1.0.0 and 1.1.0 shipped to PyPI only). Going forward, every version bump creates a corresponding git tag and GitHub Release.

### Context
- Work tracked under `Xepayac/TRUGS-DEVELOPMENT#1525` (P0 polish for `TRUGS-LLC/TRUGS-AGENT`). EPIC: `Xepayac/TRUGS-DEVELOPMENT#1548` (Bring TRUGS-LLC public portfolio to Dark Code compliance).
- Follow-up: `Xepayac/TRUGS-DEVELOPMENT#1567` — publish `trugs-tools` to PyPI so CI can restore the full `trugs-folder-check` (currently uses an inline Python fallback).

## [1.1.0] - 2026-04-08

First published after initial npm/pip install bring-up. Details pre-date this CHANGELOG — see git history and PyPI release notes at [pypi.org/project/trugs-agent/1.1.0](https://pypi.org/project/trugs-agent/1.1.0/) and npm `create-trugs-agent@1.1.0`.

## [1.0.0] - 2026-04-08

Initial public release on PyPI (`trugs-agent`) and npm (`create-trugs-agent`). Ships the TRUGS Agent instruction kit:

- `AGENT.md` — root system prompt, TRUG/L vocabulary (190 words), grammar, parsing rules
- Component folders: `AAA/`, `EPIC/`, `MEMORY/`, `FOLDER/`, `TRUGGING/`, `WEB_HUB/`, `SKILLS/`, `NDA/`
- `tools/validate.py` — vendored TRUGS CORE validator (16 rules)
- `installers/npm/` — `npx create-trugs-agent` wrapper
- `installers/pip/` — `trugs-agent-init` wrapper
- Support for Claude Code, Cursor, GitHub Copilot
