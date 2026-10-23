# hello

The smallest sentence, graph and canonical sentence again. The trap is assuming a valid graph proves runtime behaviour. `hello` names the validating party.

```trl
PARTY hello VALIDATE.
```

```sh
bash examples/hello/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: hello\n"} -->

Expected stdout: `PASS: hello`; exit status 0.
