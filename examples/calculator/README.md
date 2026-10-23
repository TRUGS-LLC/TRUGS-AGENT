# calculator

This is a walkthrough into [TRUGS-ACCOUNTING-CALCULATOR](https://github.com/TRUGS-LLC/TRUGS-ACCOUNTING-CALCULATOR),
not a copy. Read its README for the offline Rust build, then validate its invoice
text and use its check command on the visible invoice cases. Its compiler owns
the compute vocabulary; use that compiler, rather than the core TRL compiler,
for calculator programs. `calculator_instructions` is that repository's README.
The trap is assuming an accounting graph is automatically a core-language graph.
All its cases are invented calculations. The check here uses a prepared checkout,
builds in temporary storage and matches the README's six agreed invoice cases.

```trl
AGENT reader SHALL READ FILE calculator_instructions.
```

```sh
bash examples/calculator/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: calculator\n"} -->

Expected stdout: `PASS: calculator`; exit status 0.
