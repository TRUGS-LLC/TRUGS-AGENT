---
name: validate
description: Read the rule and exit status; a schema-valid graph does not prove a program correct.
---

# validate

Bindings: `learner` is the agent; `sentence`, `graph` and `invalid_graph` are lesson
artifacts; `rule` is the validator's named error; `folder` is the sample directory;
`calculator_instructions` is the calculator README linked by the map.

```trl
AGENT learner SHALL VALIDATE RECORD graph.
```

Read the rule and exit status; a schema-valid graph does not prove a program correct.

Example: [the worked lesson](../../../examples/hello/README.md).
From the repository root:

```sh
python tools/lesson.py validate
```
<!-- expect: {"status": 0, "stdout": "PASS: validate\n"} -->

Expected stdout: `PASS: validate`; exit status 0.
