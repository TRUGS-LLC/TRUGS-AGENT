---
name: compile-decompile
description: Compile, validate, decompile, recompile and compare the graph structure.
---

# compile-decompile

Bindings: `learner` is the agent; `sentence`, `graph` and `invalid_graph` are lesson
artifacts; `rule` is the validator's named error; `folder` is the sample directory;
`calculator_instructions` is the calculator README linked by the map.

```trl
AGENT learner SHALL DERIVE RECORD graph FROM RECORD sentence.
```

Compile, validate, decompile, recompile and compare the graph structure.

Example: [the worked lesson](../../../examples/hello/README.md).
From the repository root:

```sh
bash examples/hello/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: hello\n"} -->

Expected stdout: `PASS: hello`; exit status 0.
