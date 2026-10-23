---
name: run-calculator
description: Follow the calculator README; its compute vocabulary uses its own compiler and offline vendored Rust build.
---

# run-calculator

Bindings: `learner` is the agent; `sentence`, `graph` and `invalid_graph` are lesson
artifacts; `rule` is the validator's named error; `folder` is the sample directory;
`calculator_instructions` is the calculator README linked by the map.

```trl
AGENT learner SHALL READ FILE calculator_instructions.
```

Follow the calculator README; its compute vocabulary uses its own compiler and offline vendored Rust build.

Example: [the worked lesson](../../../examples/calculator/README.md).
From the repository root:

```sh
bash examples/calculator/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: calculator\n"} -->

Expected stdout: `PASS: calculator`; exit status 0.
