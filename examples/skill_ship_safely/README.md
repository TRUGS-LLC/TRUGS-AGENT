# skill_ship_safely

Reused safe-shipping contract: `dev` is the agent, `summary` is a record, `main` and `repository` are endpoints. The trap is publishing confidential data. This example expresses restrictions; it supplies no publishing automation.

```trl
AGENT dev SHALL_NOT MERGE ANY RESOURCE TO ENDPOINT main.
AGENT dev SHALL WRITE THE RECORD summary.
AGENT dev SHALL_NOT POST ANY CONFIDENTIAL DATA TO ENDPOINT repository.
```

```sh
bash examples/skill_ship_safely/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: skill_ship_safely\n"} -->

Expected stdout: `PASS: skill_ship_safely`; exit status 0.
