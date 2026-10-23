# logic-graph

A logic graph describes things, actions and their relationships. Other fields use
code graph, control-flow graph, process map, system model, design by contract, and
the C4 model's context, container, component and code levels.

Read system structure first, then the component index, then a file contract, then
an inline function contract. Above the file boundary use graphs for structure;
inside it use TRL for behaviour. One index read avoids opening every file.
Use the [folder mapping lesson](../map-a-folder/README.md) for an observed index;
it records structure, not a guarantee about program meaning.

The first sentence describes authentication: `handler` is the service, `user`
the party, `account` the data and `output` the endpoint. The second is a non-code
library process: `librarian` reads a request, matches a book and writes a receipt.
The trap is treating a graph of dependencies as an implementation of obligations.
The [todo program](../todo-app/README.md) shows the file/inline boundary.

```trl
SERVICE handler SHALL AUTHENTICATE PARTY user
  THEN READ DATA account THEN WRITE RESULT TO ENDPOINT output.
PROCESS librarian SHALL READ FILE request
  THEN MATCH RECORD book THEN WRITE RESULT TO FILE receipt.
```

```sh
bash examples/logic-graph/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: logic-graph\n"} -->

Expected stdout: `PASS: logic-graph`; exit status 0.
