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

The shell variable `repositories` names the absolute path to the prepared public
repository directory. The optional shell variable `calculator_source` names a
prepared calculator source copy; when unset, the checkout in `repositories` is used.
Set `repositories` to your offline bundle's repository directory before running:

```sh
bash examples/calculator/check.sh --repositories "$repositories" --calculator-source "${calculator_source:-$repositories/TRUGS-ACCOUNTING-CALCULATOR}"
```
<!-- expect: {"status": 0, "stdout": "PASS: calculator\n"} -->

Expected stdout: `PASS: calculator`; exit status 0.
