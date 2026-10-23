---
name: map-a-folder
description: Read one generated index before every file. The map records observed links and imports.
---

# map-a-folder

Bindings: `learner` is the agent; `sentence`, `graph` and `invalid_graph` are lesson
artifacts; `rule` is the validator's named error; `folder` is the sample directory;
`calculator_instructions` is the calculator README linked by the map.

```trl
AGENT learner SHALL MAP MODULE folder TO RECORD graph.
```

Read one generated index before every file. The map records observed links and imports.

Example: [the worked lesson](../../../examples/map-a-folder/README.md).
From the repository root:

```sh
bash examples/map-a-folder/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: map-a-folder\n"} -->

Expected stdout: `PASS: map-a-folder`; exit status 0.
