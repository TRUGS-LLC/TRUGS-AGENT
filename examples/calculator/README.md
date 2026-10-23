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

The shell variable `repositories` names the absolute path to the prepared public
repository directory. The optional shell variable `calculator_source` names a
prepared calculator source copy; when unset, the checkout in `repositories` is used.
Set `repositories` to your offline bundle's repository directory before running:

```sh
bash examples/calculator/check.sh --repositories "$repositories" --calculator-source "${calculator_source:-$repositories/TRUGS-ACCOUNTING-CALCULATOR}"
```
<!-- expect: {"status": 0, "stdout": "PASS: calculator\n"} -->

Expected stdout: `PASS: calculator`; exit status 0.
