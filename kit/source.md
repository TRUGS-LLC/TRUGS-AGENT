# TRUGS agent entry

Bindings: `agent` is the agent reading this file; `entry` is
[README.md](https://github.com/TRUGS-LLC/TRUGS-AGENT/blob/main/README.md);
`primer` is [PRIMER.md](https://github.com/TRUGS-LLC/TRUGS-AGENT/blob/main/PRIMER.md);
`map` is [map/published.trl](https://github.com/TRUGS-LLC/TRUGS-AGENT/blob/main/map/published.trl);
`version_changed` means the installed trugs-tools version differs from the version
under which the agent last read README.md and map/published.trl.
`language` is trugs_tools/data/language.trug.json in the installed package.
`sentence` is the instruction being authored; `graph` is its compiled TRUGS graph.

```trl
AGENT agent SHALL READ FILE entry.
AGENT agent SHALL READ FILE primer ONCE.
AGENT agent SHALL READ FILE map SUBJECT_TO DATA version_changed
  THEN READ FILE entry.
AGENT agent SHALL READ FILE language THEN WRITE RECORD sentence.
AGENT agent SHALL VALIDATE RECORD graph.
```

Use TRL when communicating instructions; store and validate the graph as JSON.
Read an example or skill when the task calls for it. Read the map when a question
concerns another repository. The version directive is a reading rule; no background
version monitor or memory store is installed.

Dependency: trugs-tools `>=2.4.0,<3`.
Use trugs-agent check after placing these files. The self-check compiles hello,
validates, decompiles, recompiles, compares and checks placed instruction vocabulary.

Pointers: [logic graphs](https://github.com/TRUGS-LLC/TRUGS-AGENT/tree/main/examples/logic-graph),
[folder mapping](https://github.com/TRUGS-LLC/TRUGS-AGENT/tree/main/examples/map-a-folder),
[calculator](https://github.com/TRUGS-LLC/TRUGS-ACCOUNTING-CALCULATOR),
[web graphs](https://github.com/TRUGS-LLC/TRUGS-WEB),
[language](https://github.com/TRUGS-LLC/TRUGS), and the coming TRUGS-LAW repository.

{{VOCABULARY}}
