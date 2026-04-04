# WEB_HUB — Agent Instructions

<trl>
DEFINE "WEB_HUB" AS DATA graph 'for RECORD web_resource.
EACH DATA node SHALL CONTAIN RECORD url AND RECORD purpose AND RECORD category.
EACH DATA edge SHALL CONTAIN RECORD relation AND RECORD weight FROM 0.0 TO 1.0.
AGENT SHALL READ DATA graph WEB_HUB TO NAVIGATE RECORD web_landscape.
AGENT SHALL_NOT FETCH RECORD url UNLESS RECORD purpose MATCHES RECORD task.
</trl>

A WEB_HUB is a TRUG that indexes web resources — papers, repos, tools, articles, standards — organized into branches with weighted edges showing how things relate.

---

## Structure

<trl>
DEFINE "branch" AS MODULE CONTAINING RESOURCE node 'for A RECORD audience.
EACH DATA graph WEB_HUB SHALL CONTAIN ONE OR MORE MODULE branch.
EACH MODULE branch SHALL CONTAIN RESOURCE node 'with RECORD url AND RECORD purpose.
DATA edge 'between RESOURCE SHALL CONTAIN RECORD weight AND RECORD relation.
RECORD weight SHALL RANK RECORD relevance — HIGHER 'is MORE RELEVANT.
</trl>

A web hub has three levels:

| Level | Type | Purpose |
|-------|------|---------|
| Root | FOLDER | The hub itself — contains branches |
| Branch | MODULE | Audience-specific grouping of resources |
| Resource | RESOURCE | A single URL with purpose and category |

### Resource Node Properties

<trl>
EACH RESOURCE node SHALL CONTAIN RECORD name — TITLE 'of RESOURCE.
EACH RESOURCE node SHALL CONTAIN RECORD url — EXACT RECORD address.
EACH RESOURCE node SHALL CONTAIN RECORD purpose — A RECORD sentence EXPLAINING WHAT RESOURCE CONTAINS AND WHY IT MATTERS.
EACH RESOURCE node SHALL CONTAIN RECORD category — PAPER OR REPO OR ARTICLE OR TOOL OR STANDARD OR GUIDE OR TEMPLATE OR INFLUENCER.
</trl>

The `purpose` field is the key — it tells you what the resource contains without fetching it. Read purposes to decide relevance before opening any URL.

---

## Edge Relations

<trl>
DEFINE "MOTIVATES" AS DATA edge — THIS RESOURCE IDENTIFIES A RECORD problem 'that TARGET SOLVES.
DEFINE "CONTRASTS" AS DATA edge — THIS RESOURCE DOES RECORD similar_thing BUT DIFFERENTLY.
DEFINE "COMPLEMENTS" AS DATA edge — THIS RESOURCE WORKS ALONGSIDE TARGET.
DEFINE "CONTEXTUALIZES" AS DATA edge — THIS RESOURCE SHOWS THE RECORD landscape.
DEFINE "EXTENDS" AS DATA edge — THIS RESOURCE BUILDS 'on TARGET.
DEFINE "AMPLIFIES" AS DATA edge — THIS RESOURCE INCREASES RECORD reach 'of TARGET.
DEFINE "IMPLEMENTS" AS DATA edge — THIS RESOURCE 'is AN IMPLEMENTATION 'of TARGET.
DEFINE "FEEDS" AS DATA edge — BRANCH CONVERGES 'on TARGET.
</trl>

| Relation | Weight Range | Meaning |
|----------|-------------|---------|
| MOTIVATES | 0.6–0.95 | Resource identifies the problem your project solves |
| CONTRASTS | 0.5–0.8 | Resource does something similar but different — competitive landscape |
| COMPLEMENTS | 0.5–0.85 | Resource works alongside yours — integration opportunity |
| CONTEXTUALIZES | 0.5–0.7 | Resource shows the broader landscape |
| EXTENDS | 0.7–0.9 | Resource builds on another resource |
| AMPLIFIES | 0.8–0.9 | Resource increases reach — influencers, channels |
| IMPLEMENTS | 0.9–1.0 | Resource is a concrete implementation of a spec or paper |
| FEEDS | 1.0 | Branch → convergence node (structural) |

**Higher weight = stronger connection.** When traversing, follow high-weight edges first.

---

## How to Read a Web Hub

<trl>
AGENT SHALL READ DATA graph web.trug.json 'at ENTRY RECORD research_task.
AGENT SHALL IDENTIFY ALL MODULE branch TO UNDERSTAND RECORD landscape_structure.
AGENT SHALL FOLLOW DATA edge 'with RECORD weight ABOVE 0.8 FIRST.
AGENT SHALL READ RECORD purpose 'on EACH RESOURCE 'before FETCH RECORD url.
AGENT SHALL_NOT FETCH ALL RESOURCE — ONLY FETCH RECORD relevant RESOURCE.
</trl>

1. **Read the branches** — understand how resources are organized by audience
2. **Follow high-weight edges** — these are the strongest connections
3. **Read purposes** — decide relevance before fetching any URL
4. **Traverse by relation type** — MOTIVATES edges find the problem, CONTRASTS edges find alternatives, COMPLEMENTS edges find integration partners

---

## How to Build a Web Hub

<trl>
AGENT SHALL IDENTIFY RECORD audience 'for EACH MODULE branch.
'for EACH MODULE branch AGENT SHALL RESEARCH 10 TO 20 RESOURCE.
EACH RESOURCE SHALL 'have RECORD url 'that EXISTS AND RECORD purpose 'that 'is SPECIFIC.
AGENT SHALL CREATE DATA edge 'with RECORD weight 'for EACH RECORD relationship 'between RESOURCE.
AGENT SHALL VALIDATE DATA graph web.trug.json.
</trl>

### Step by Step

1. **Define branches** — who are the audiences? What pain point brings each audience to your project?
2. **Research resources** — for each branch, find 10-20 high-quality resources: papers, repos, tools, articles, standards
3. **Write purposes** — one sentence per resource explaining what it contains AND why it matters to your project
4. **Create edges** — how do resources relate to each other and to your project? Weight by relevance
5. **Validate** — run the validator to check graph correctness

### Resource Categories

<trl>
DEFINE "PAPER" AS RECORD category — ACADEMIC RESEARCH OR TECHNICAL REPORT.
DEFINE "REPO" AS RECORD category — GITHUB REPOSITORY OR CODE PROJECT.
DEFINE "ARTICLE" AS RECORD category — BLOG POST OR TECHNICAL ARTICLE.
DEFINE "TOOL" AS RECORD category — SOFTWARE TOOL OR GENERATOR.
DEFINE "STANDARD" AS RECORD category — FORMAL STANDARD OR SPECIFICATION.
DEFINE "GUIDE" AS RECORD category — HOWTO OR BEST PRACTICES.
DEFINE "TEMPLATE" AS RECORD category — REUSABLE STARTING POINT.
DEFINE "INFLUENCER" AS RECORD category — PERSON OR CHANNEL 'with RECORD audience.
</trl>

---

## Updating a Web Hub

<trl>
IF AGENT DISCOVER RELEVANT RECORD web_resource THEN AGENT MAY ADD RESOURCE node.
EACH NEW RESOURCE node SHALL CONTAIN RECORD url AND RECORD purpose AND RECORD category.
AGENT SHALL CREATE DATA edge 'with RECORD weight TO EXISTING RESOURCE OR MODULE.
AGENT SHALL_NOT ADD RESOURCE WITHOUT RECORD purpose — PURPOSE 'is REQUIRED.
AGENT SHALL VALIDATE DATA graph AFTER EACH UPDATE.
</trl>

- **New resource found** — add a RESOURCE node with url, purpose, category. Create edges to related resources.
- **Resource gone** — set `stale: true` on the node. Don't remove it — the edges still show the relationship.
- **Better resource found** — add the new one, create an `SUPERSEDES` edge to the old one.

---

## Example

See the main `web.trug.json` in this folder — 3 branches (Structured Agent, Graph Native, Agent Protocols), 54 nodes, 51 edges, 10 relation types. Also see `NDA/web.trug.json` for a domain-specific example (NDA research — templates, legal guidance, tools, WA state statutes).
