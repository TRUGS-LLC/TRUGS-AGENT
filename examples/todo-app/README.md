# todo-app

The program example for the logic-graph guide. `create_todo`, `list_todos` and `complete_todo` name Python functions; `todos` is the collection. The trap is placing a state assignment into identifier syntax. The check validates the contract, runs the program and verifies invalid titles and missing identifiers.

```trl
FUNCTION create_todo SHALL VALIDATE RECORD input
  THEN WRITE VALID RECORD TO DATA todos.
FUNCTION create_todo SHALL_NOT WRITE INVALID RECORD.
FUNCTION list_todos SHALL READ ALL RECORD FROM DATA todos
  THEN FILTER RESULT.
FUNCTION complete_todo SHALL MATCH RECORD todo
  THEN WRITE VALID RECORD TO DATA todos.
```

```sh
bash examples/todo-app/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: todo-app\n"} -->

Expected stdout: `PASS: todo-app`; exit status 0.
