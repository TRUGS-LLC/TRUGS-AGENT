---
name: write-trl
description: Write an actor, modal and verb before naming the artifacts. Look up words in the installed language file.
---

# write-trl

Bindings: `learner` is the agent; `sentence`, `graph` and `invalid_graph` are lesson
artifacts; `rule` is the validator's named error; `folder` is the sample directory;
`calculator_instructions` is the calculator README linked by the map.

```trl
AGENT learner SHALL WRITE RECORD sentence.
```

Write an actor, modal and verb before naming the artifacts. Look up words in the installed language file.

Example: [the worked lesson](../../../examples/hello/README.md).
From the repository root:

```sh
bash examples/hello/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: hello\n"} -->

Expected stdout: `PASS: hello`; exit status 0.
