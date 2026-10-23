# Fixed tasks and general questions

[items.json](items.json) holds prompts and expected answers. Each answer identifies
its source: the TRUGS README, a command's help, or the installed language file.
The kit checker verifies those source statements; it does not ask an agent to
answer the tasks. No evaluation run is part of building this candidate.

For a later clean-machine run, give an agent only the onboarding entry, then the
prompts without their answers. Compare responses against the cited sources and
retain the results separately before deciding publication.
