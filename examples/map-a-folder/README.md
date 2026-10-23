# map-a-folder

An agent saves effort by reading one index instead of every source file.
`folder` is the input directory and `index` the generated record. trugs-web map
records files, folders, references and local imports, not inferred behaviour.
The checker maps the [sample folder](sample/README.md) offline, validates it,
decompiles and validates the recompiled sentence. File hashes and other
non-language metadata are not preserved by TRL. Choose an output outside the mapped folder.
Symlinks are recorded by link text, and sources are never fetched.
This lesson uses trugs-web 2.1.0, installed from the Python package index as shown
in the entry. The trap is including the output in its own input.

```trl
PROCESS mapper SHALL MAP MODULE folder TO RECORD index.
```

```sh
bash examples/map-a-folder/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: map-a-folder\n"} -->

Expected stdout: `PASS: map-a-folder`; exit status 0.
