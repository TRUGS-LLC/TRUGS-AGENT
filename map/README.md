# Published repository map

`reader` is the agent. Each group in [published.trl](published.trl) has one row
below binding its resource, status, role, installation route and instruction entry.
The [compiled graph](published.trug.json) contains these same sentence groups.
The map points to each repository; it does not copy its instructions.

| Resource | Group and role | Source revision | Installation | Own instructions |
|---|---|---|---|---|
| [trugs](https://github.com/TRUGS-LLC/TRUGS) | `live_specification`: Instruct; specification and four-type overview | 37bb78c7 | Read the repository directly; the specification needs no installation. | [README.md](https://github.com/TRUGS-LLC/TRUGS/blob/main/README.md) |
| [tools](https://github.com/TRUGS-LLC/TRUGS-TOOLS) | `live_language_tools`: Instruct; core language CLI | a0a4218f | Python package trugs-tools 2.4.0 provides trug. | [README.md](https://github.com/TRUGS-LLC/TRUGS-TOOLS/blob/main/README.md) |
| [store](https://github.com/TRUGS-LLC/TRUGS-STORE) | `live_graph_storage`: Instruct support; graph storage backends | f363268b | Python package trugs-store 2.2.0. | [README.md](https://github.com/TRUGS-LLC/TRUGS-STORE/blob/main/README.md) |
| [calculator](https://github.com/TRUGS-LLC/TRUGS-ACCOUNTING-CALCULATOR) | `live_compute`: Compute; accounting calculator | b806f115 | Build with the repository README and a Rust toolchain; crates are vendored. | [README.md](https://github.com/TRUGS-LLC/TRUGS-ACCOUNTING-CALCULATOR/blob/main/README.md) |
| [site](https://github.com/TRUGS-LLC/TRUGS-SITE) | `live_specification_site`: Describe support; static specification website | d2de19cb | Read index.html; no build step or package installation. | [README.md](https://github.com/TRUGS-LLC/TRUGS-SITE/blob/main/README.md) |
| [web](https://github.com/TRUGS-LLC/TRUGS-WEB) | `live_describe`: Describe; folder and web graphs | 9b6cd1f60e1deaa03073f89c78f1f6d5ae277e28 | Install trugs-web 2.1.0 from the Python package index. Local folder mapping is offline. | [README.md](https://github.com/TRUGS-LLC/TRUGS-WEB/blob/main/README.md) |
| [viewer](https://github.com/TRUGS-LLC/TRUGS-VIEWER) | `demonstration`: Describe; a demonstration, not in active development | c27e39fe | Open https://trugs-llc.github.io/TRUGS-VIEWER/ in a browser; no package installation. | [README.md](https://github.com/TRUGS-LLC/TRUGS-VIEWER/blob/main/README.md) |
| [trl](https://github.com/TRUGS-LLC/TRUGS-TRL) | `coming_language`: Instruct; coming, with no date | coming | Coming; no installation route yet. | Coming; no published instruction entry |
| [law](https://github.com/TRUGS-LLC/TRUGS-LAW) | `coming_law`: Instruct; coming, with no date | coming | Coming; no installation route yet. | Coming; no published instruction entry |
| [agent_kit](https://github.com/TRUGS-LLC/TRUGS-AGENT) | `live_onboarding`: Instruct support; onboarding kit | this checkout | Install trugs-agent 2.0.0 from the Python package index. | [AGENTS.md](https://github.com/TRUGS-LLC/TRUGS-AGENT/blob/main/AGENTS.md) |

The revisions identify the sources for the published packages and repositories.
Install the language tools in the entry's stated range; the map records the 2.4.0
source used to check this kit. The viewer opens generated graphs in a browser.
For a repository with no separate agent instructions, its own README is the entry.
The Govern runner is coming, with no repository or date promised here.
