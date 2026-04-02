# WEB_HUB — Curated Web Resource Graph

A TRUG graph that indexes the web landscape around TRUGS-AGENT. Nodes are URLs — papers, repos, tools, articles, standards. Edges show how they relate. Weights rank importance.

## Three Branches

| Branch | Audience | Entry Point |
|--------|----------|-------------|
| **Structured Agent** | LLM developers frustrated with prompt drift | TRL + TRUGGING |
| **Graph Native** | Engineers building with knowledge graphs and code graphs | FOLDER + TRUGGING |
| **Agent Protocols** | Teams building reliable agent systems | AAA + MEMORY + EPIC |

All three branches converge on TRUGS-AGENT — each audience discovers it through their own pain point.

## How to Use

Your LLM reads `web.trug.json` to navigate the landscape:
- Find related work for a blog post
- Pull citations for a paper
- Answer "what's the state of the art in X?"
- Identify gaps where TRUGS-AGENT is the only solution

Edge weights (0.0–1.0) rank relevance to the TRUGS-AGENT story. Higher weight = stronger connection.

## Structure

`web.trug.json` contains three branch nodes, each containing 12-18 resource nodes. Resources link to each other and to TRUGS-AGENT components via weighted edges.
