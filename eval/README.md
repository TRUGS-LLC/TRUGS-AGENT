# Fixed tasks and general questions

[items.json](items.json) holds prompts and expected answers. Each answer identifies
its source: the TRUGS README, a command's help, or the installed language file.
The kit checker verifies those source statements; it does not ask an agent to
answer the tasks. The source check is separate from an evaluation run.

For a clean-machine run, install trugs-agent 2.0.0 and trugs-web 2.1.0 from the
Python package index with the language tools in the entry's stated range. Give an
agent only the onboarding entry, then the prompts without their answers. Compare
responses against the cited sources and retain the results separately.
