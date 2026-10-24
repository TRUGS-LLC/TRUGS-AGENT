# skill_refactor_safely

Reused safe-refactor contract: `dev` is the acting agent, `tests` is the result record, a public interface is protected, and `main` is a destination endpoint. The trap is putting an obligation on the interface rather than the agent. The check preserves the original canonical sentences.

```trl
AGENT dev SHALL VALIDATE THE RECORD tests.
AGENT dev SHALL_NOT UPDATE ANY PUBLIC INTERFACE.
AGENT dev SHALL_NOT MERGE ANY RESOURCE TO ENDPOINT main.
```

```sh
bash examples/skill_refactor_safely/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: skill_refactor_safely\n"} -->

Expected stdout: `PASS: skill_refactor_safely`; exit status 0.
