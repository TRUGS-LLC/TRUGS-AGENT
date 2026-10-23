# refactor_a_program

A refactoring obligation reads a legacy module, derives a focused function and writes a refactored module. The guard forbids leaving the test suite failed. These names are bindings to a hypothetical billing module; this lesson compiles the contract, rather than performing that refactor. The trap is mistaking a contract for the tests themselves.

```trl
PROCESS refactorer SHALL READ FILE legacy_module
  THEN DERIVE FUNCTION get_due_invoices
  THEN WRITE RESULT TO FILE refactored_module.
PROCESS refactorer SHALL_NOT MAP ANY FUNCTION TO FAILED DATA test_suite.
```

```sh
bash examples/refactor_a_program/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: refactor_a_program\n"} -->

Expected stdout: `PASS: refactor_a_program`; exit status 0.
