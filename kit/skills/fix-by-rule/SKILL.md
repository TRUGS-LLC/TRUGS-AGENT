---
name: fix-by-rule
description: The CONSTRAINT_REQUIRES_ACTOR error means an obligation was placed on a non-Actor. Replace that subject with an Actor and validate again.
---

# fix-by-rule

Bindings: `learner` is the agent; `sentence`, `graph` and `invalid_graph` are lesson
artifacts; `rule` is the validator's named error; `folder` is the sample directory;
`calculator_instructions` is the calculator README linked by the map.

```trl
AGENT learner SHALL REPLACE RECORD invalid_graph SUBJECT_TO DATA rule.
```

The CONSTRAINT_REQUIRES_ACTOR error means an obligation was placed on a non-Actor. Replace that subject with an Actor and validate again.

Example: [the worked lesson](../../../examples/hello/README.md).
From the repository root:

```sh
python tools/lesson.py fix
```
<!-- expect: {"status": 0, "stdout": "PASS: CONSTRAINT_REQUIRES_ACTOR fixed\n"} -->

Expected stdout: `PASS: CONSTRAINT_REQUIRES_ACTOR fixed`; exit status 0.
