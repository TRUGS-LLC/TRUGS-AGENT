---
source_issue: Xepayac/TRUGS-DEVELOPMENT#1432
pushed_down_at: 2026-05-09
destination: TRUGS-LLC/TRUGS-AGENT/PROPOSAL/
push_down_reason: Repo-specific work — belongs in this repo per the 2026-05-09 issue-triage walkthrough.
created: 2026-04-09
updated: 2026-04-09
labels: (none)
---

# BOOK: Graph-First Development with TRUGS — developer tutorial for code-as-graph workflow

> **Push-down 2026-05-09.** Captured from [`Xepayac/TRUGS-DEVELOPMENT#1432`](https://github.com/Xepayac/TRUGS-DEVELOPMENT/issues/1432) verbatim during the 2026-05-09 issue-triage walkthrough. The original issue has been closed; this file is the working surface in this repo.

---

## Original body

## Vision

Developers need a guided tutorial to transition from file-based to graph-based development. TRUGS-AGENT teaches agents. This book teaches humans.

**Core thesis:** Your LLM agent understood this system in one prompt. This book teaches you what the agent already knows — and why the safety system around the graph is what makes agent-written code production-ready.

**Four-leg table (woven through every chapter, not a standalone section):**
1. **TRUG** — the graph structure (what exists, how it connects)
2. **Testing** — automated verification (does it work?)
3. **Auditing** — cyclic review (does it match the plan? is it secure?)
4. **HITM** — human judgment at every boundary (should this ship?)

Remove any leg and the table falls. The TRUG makes testing/auditing/HITM work at scale. Testing/auditing/HITM make the TRUG safe. Together they give LLM agents the guardrails to write productive code.

## Structure

**Part 1 — What Changes (and What Doesn't)**
- Ch 1: Your agent already gets it (LLMs read graphs natively — files are the bottleneck)
- Ch 2: Files are serialization (you don't edit .o files either)
- Ch 3: Your first TRUG — a function with edges instead of comments
- Ch 4: The four-leg table — why the graph alone isn't enough

**Part 2 — The 190 Words**
- Ch 5: Nouns — the things that exist in your code
- Ch 6: Verbs — what your code does
- Ch 7: Modals — SHALL, MAY, SHALL_NOT (obligations, not suggestions)
- Ch 8: Your first TRL contract (side-by-side: docstring vs TRL)

**Part 3 — Working in the Graph**
- Ch 9: Navigating instead of browsing (graph explorer, not file tree)
- Ch 10: Creating nodes — with tests and audit from the start
- Ch 11: Edges as documentation (IMPLEMENTS, DEPENDS_ON, FEEDS)
- Ch 12: Compilation — the graph renders to files, the compiler runs, done

**Part 4 — Working with Others (Humans and Agents)**
- Ch 13: PROPOSE, VOTE, MERGE — code review as protocol, with HITM gates
- Ch 14: Trust modes — your laptop vs the team server
- Ch 15: The agent sitting next to you — same graph, same rules, same audit
- Ch 16: The four legs in practice — agent writes, tests verify, audit catches drift, human approves

## Arc

The reader isn't learning a new tool. They're learning how to make their LLM agent productive and safe. The TRUG is the structure. Testing, auditing, and HITM are the guardrails. Together: agent-written production code.

## Approach

- Every chapter ends with a hands-on exercise in the VS Code extension
- Side-by-side comparisons: old way (file/comment) vs new way (node/TRL)
- Four-leg system woven through every example — never just "here's the graph"
- No theory without a working example
- Assumes: competent developer, no TRUGS knowledge, possibly no LLM experience
- Published to TRUGS-LLC, Apache 2.0

## Dependencies

- TRUGS_CODE extension working (#1421 ✅)
- TRUGS_PORT server with graph navigation
- noise-chatbot framework for chat examples
- Code-as-graph-property architecture (decision captured 2026-04-08)

---

## Comments (5 total)

### Comment 1 — @Xepayac on 2026-04-09

## Case Studies (real projects, real git history)

Thread these through the chapters as worked examples, not a standalone section:

1. **Session-Router clean room** — C++ to Go rewrite. Xepayac wrote spec, Copilot implemented. Clean room wall: spec author never touches code, implementor never reads C++ source. TRUG navigated the codebase, 106 tests validated QUIC layer, audits caught issues, HITM at every boundary. (#1286)

2. **Noise Chatbot** — Architecture to published Apache 2.0 product in one session. Template-only LLM (classifies, never composes), 5-tier honeypot defense, 22 tests, cyclic audit with code quality + plan compliance, PR waiting for human merge. Agent never drifted because the plan was a TRUG and audit checked compliance. (TRUGS-LLC/noise-chatbot)

3. **TRUGS_OS** — VLM agent navigating Wikipedia in a QEMU VM. Multi-turn tool_use chains, task TRUGs for autonomous execution, 8 PRs across 9 issues. Three-tier interaction (API 90% / Vision 9% / HITM 1%). (#1385, #1392)

4. **VS Code Extension** — Cross-language Noise_IK interop (TypeScript ↔ Go), noise-helper bridge pattern, thin IDE with zero local storage. Three debugging attempts before finding split-state swap. The TRUG tracked what was tried and why. (#1421)

Each case study demonstrates all four legs working together. The git history is the proof.

### Comment 2 — @Xepayac on 2026-04-09

## Clarification: Two tiers of evidence

**Full case studies (dedicated sections, verifiable git history):**
- Session-Router clean room — study already started, public repo with PRs and commits
- Noise Chatbot — TRUGS-LLC/noise-chatbot, PR #1, 22 tests, complete defense system

**Inline examples (referenced throughout chapters, no standalone writeup):**
- TRUGS_OS — multi-turn VLM, task TRUGs, QEMU (#1385, #1392)
- VS Code extension — cross-language Noise, noise-helper bridge (#1421)
- Merge engine — three-way diff, cyclic audit (#1408)
- Guide v0.6.0 — document structure as a TRUG, section-level tracking (#1425)

Full studies are proof. Inline examples are illustrations. Both link to real PRs.

### Comment 3 — @Xepayac on 2026-04-09

## Flagship Worked Example: Blackjack Advantage Play Simulator

Existing spec: `LIBRARY/REFERENCE_trugs_test.md` (1,109 lines, 64 deliverables, complete blackjack + Spanish 21 + AP rules)

**Why this example:**
- Every developer understands the domain (unlike QUIC routing)
- The spec already exists — months of manual research
- 64 deliverables = complex enough to prove the system works
- Monte Carlo simulation (100K-1M iterations) = computationally verifiable results
- Original manual effort: months. Expected with four-leg system: 20-40 minutes.

**How it threads through the book:**
- Part 1: "This spec took months. Watch what happens next."
- Part 2: TRL contracts for rules, strategies, simulation engine
- Part 3: Graph structure — rule nodes, strategy nodes, DEPENDS_ON/IMPLEMENTS edges
- Part 4: Full AAA walkthrough — VISION→FEASIBILITY→SPEC→CODE→TEST→AUDIT→HITM

This example will be developed live as part of writing the book — the git history of building it IS the chapter content.

### Comment 4 — @Xepayac on 2026-04-09

## Research as Graph Construction — Web TRUG in the workflow

The agent doesn't just code from the spec — it extends the spec by searching.

**In the blackjack example:**
- Search for obscure rule variations (Nevada, Atlantic City, Macau, online) → rule nodes with SUBJECT_TO jurisdiction edges
- Search for mathematically proven randomization (Fisher-Yates + CSPRNG) → academic reference nodes
- Search for advanced count systems (Omega II, Wong halves) → strategy nodes with REFERENCES to source
- Search for gaming commission payout tables → validation data with provenance

Every search result becomes a TRUG node with REFERENCES edges to the source URL, captured in the web TRUG. The research is traceable, not lost in browser tabs.

This demonstrates: the four-leg system + web research = the agent researches, extends the spec, implements, tests, audits, and hands to human. All in under an hour. All traceable.

### Comment 5 — @Xepayac on 2026-04-09

## The Punchline (SPOILER — last chapter)

The book builds the card counting simulator across all chapters. Monte Carlo shows 1-2% edge. Reader is excited.

Last chapter: "One more thing. Let's add current tax rules."

Agent researches gambling tax regulations via web TRUG → adds SUBJECT_TO tax_jurisdiction constraint nodes → reruns Monte Carlo → edge goes negative.

Card counting doesn't work anymore. The math works. The profit doesn't survive taxes.

**Why this matters for the book's thesis:**
- A human developer would have shipped without tax rules
- The research + audit loop caught a real-world constraint that changes the answer
- The system found something the developer didn't think to look for
- This is the difference between "I built a tool" and "the system built the right tool"

Do NOT spoil this in earlier chapters. Let the reader get invested.
