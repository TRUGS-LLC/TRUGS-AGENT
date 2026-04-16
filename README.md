[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![TRUGS v1.0](https://img.shields.io/badge/TRUGS-v1.0-green.svg)](https://github.com/TRUGS-LLC/TRUGS)
[![Works with Claude Code](https://img.shields.io/badge/Works_with-Claude_Code-blueviolet.svg)](https://claude.ai/code)
[![Works with Cursor](https://img.shields.io/badge/Works_with-Cursor-orange.svg)](https://cursor.com)
[![Works with Copilot](https://img.shields.io/badge/Works_with-GitHub_Copilot-brightgreen.svg)](https://github.com/features/copilot)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-lightgrey.svg)](#quickstart)

# TRUGS Agent

**Your LLM ignores your system prompt because English is ambiguous. TRUGS Agent gives it a formal instruction language instead.**

TRUG/L (TRUGS Language) has 190 words. Every sentence has exactly one meaning. Every instruction compiles to a verifiable graph. Your AI coding assistant stops interpreting and starts executing.

No SDK. No runtime. No dependencies. Copy one file into your project and your LLM speaks TRUG/L.

## The Problem

You write careful instructions in your `CLAUDE.md` or `.cursorrules`. Your LLM interprets them differently every time:

```
❌  "Make sure the code is clean and well-tested"
     → Sometimes adds tests, sometimes doesn't
     → "Clean" means something different every run
     → No way to verify the instruction was followed
```

## The Fix

TRUG/L instructions have exact definitions. The LLM doesn't interpret — it executes:

```
✅  <trl>
    AGENT SHALL VALIDATE ALL CODE SUBJECT_TO INTERFACE schema.
    AGENT SHALL REQUIRE RECORD test FOR EACH FUNCTION.
    AGENT SHALL_NOT DEPLOY INVALID DATA.
    </trl>

     → SHALL = must do, failure is a violation
     → VALIDATE = specific operation, not a vague suggestion
     → SUBJECT_TO = explicit dependency
     → SHALL_NOT = hard prohibition
```

Every word maps to a graph element. Every sentence is auditable. No ambiguity.

## Install

Pick your method:

```bash
# npm — one command, all files
npx create-trugs-agent                    # Claude Code (default)
npx create-trugs-agent cursor             # Cursor
npx create-trugs-agent copilot            # GitHub Copilot

# pip — same thing, Python
pip install trugs-agent
trugs-agent-init                          # Claude Code (default)
trugs-agent-init cursor                   # Cursor
trugs-agent-init copilot                  # GitHub Copilot

# curl — just the core file, nothing else
curl -o CLAUDE.md https://raw.githubusercontent.com/TRUGS-LLC/TRUGS-AGENT/main/AGENT.md

# git — clone and copy what you want
git clone https://github.com/TRUGS-LLC/TRUGS-AGENT.git
cp TRUGS-AGENT/AGENT.md your-project/CLAUDE.md
```

**Already using Cursor?** This repo includes `.cursor/rules/trugs-agent.mdc` — clone the repo and copy the `.cursor/` directory into your project.

**Validate your TRUGs:**

```bash
python tools/validate.py my_graph.trug.json          # Validate one
python tools/validate.py --all my_project/            # Validate all
```

See [examples/](examples/) for a working project with TRUGS Agent integrated.

## How It Compares

| | TRUGS Agent | LangChain | CrewAI | Pydantic AI |
|---|---|---|---|---|
| **What it is** | A language (190 words) | A Python SDK | A Python framework | A Python library |
| **Install** | Copy a file | `pip install langchain` | `pip install crewai` | `pip install pydantic-ai` |
| **Dependencies** | Zero | 50+ packages | 20+ packages | Pydantic + httpx |
| **Lock-in** | None — works with any LLM tool | LangChain ecosystem | CrewAI runtime | Pydantic AI runtime |
| **How agents get instructions** | Formal language with exact semantics | Python code chains | Role/goal strings | Type-annotated functions |
| **Instruction ambiguity** | Zero — every word has one meaning | English prompts in code | English role descriptions | English docstrings |
| **Verifiable** | Yes — compiles to auditable graph | No | No | Partial (type checking) |
| **Works with Claude Code** | Yes | No (different paradigm) | No (different paradigm) | No (different paradigm) |
| **Works with Cursor** | Yes | No (different paradigm) | No (different paradigm) | No (different paradigm) |
| **Runtime required** | No | Yes | Yes | Yes |
| **Lines of code** | 0 (it's text files) | ~100K+ | ~30K+ | ~10K+ |

**The key difference:** LangChain, CrewAI, and Pydantic AI are code frameworks — you write Python to orchestrate agents. TRUGS Agent is a language — you write instructions that any LLM tool can read. They solve different problems. If you need Python orchestration, use a framework. If you need your LLM to follow unambiguous instructions, use TRUG/L.

## Components

Every component is standalone. Start with just the root (`AGENT.md`), add components as needed:

| Folder | What It Does | When To Use It |
|--------|-------------|----------------|
| [FOLDER/](FOLDER/) | Machine-readable filesystem index as a JSON graph | You want your LLM to understand your project structure |
| [AAA/](AAA/) | 9-phase development protocol — plan, code, audit | You want structured development with quality gates |
| [EPIC/](EPIC/) | Portfolio tracker as a traversable graph | You track multiple projects or features |
| [MEMORY/](MEMORY/) | Persistent context across sessions | Your LLM forgets decisions between conversations |
| [TRUGGING/](TRUGGING/) | Describe your codebase with TRUGs at every level | You want machine-readable architecture documentation |
| [WEB_HUB/](WEB_HUB/) | Curated web resources indexed as a graph | You research tools, papers, and libraries |
| [SKILLS/](SKILLS/) | 19 composable primitives for agent workflows | You need repeatable agent actions |

### Adoption Path

```
Just the root         → TRUG/L vocabulary in any project (30 seconds)
Root + Memory         → Persistent context across sessions
Root + AAA            → Structured development with audit gates
Root + Folder         → Machine-readable project index
Root + Everything     → Complete LLM development system
```

## Full Specification

The complete TRUGS reference library lives in [TRUGS-LLC/TRUGS/REFERENCE/](https://github.com/TRUGS-LLC/TRUGS/tree/main/REFERENCE). TRUGS-AGENT is the front door; go there for depth.

### Papers and Standards

- **[PAPER_dark_code.md](https://github.com/TRUGS-LLC/TRUGS/blob/main/REFERENCE/PAPER_dark_code.md)** — the WHY: Dark Code problem and TRUGS as resolution
- **[PAPER_how_to_code_with_trugs.md](https://github.com/TRUGS-LLC/TRUGS/blob/main/REFERENCE/PAPER_how_to_code_with_trugs.md)** — the HOW: practitioner guide
- **[STANDARD_dark_code_compliance.md](https://github.com/TRUGS-LLC/TRUGS/blob/main/REFERENCE/STANDARD_dark_code_compliance.md)** — the CHECK: auditable compliance checklist
- **Foundational TRUGS Paper**: https://github.com/TRUGS-LLC/TRUGS/blob/main/PAPER/trugs.pdf — [DOI 10.5281/zenodo.19379454](https://doi.org/10.5281/zenodo.19379454)

### Reference Implementation

- **TRUG/L compiler + TRUGS toolchain**: https://github.com/TRUGS-LLC/TRUGS

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get involved. We welcome contributions of all kinds — from fixing typos to adding new components.

## License

Apache 2.0 — [TRUGS LLC](https://github.com/TRUGS-LLC)
