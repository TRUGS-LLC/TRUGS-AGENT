<!-- Generated from kit/source.md; edit the source. -->
# TRUGS agent entry

Bindings: `agent` is the agent reading this file; `entry` is
[README.md](https://github.com/TRUGS-LLC/TRUGS-AGENT/blob/main/README.md);
`primer` is [PRIMER.md](https://github.com/TRUGS-LLC/TRUGS-AGENT/blob/main/PRIMER.md);
`map` is [map/published.trl](https://github.com/TRUGS-LLC/TRUGS-AGENT/blob/main/map/published.trl);
`version_changed` means the installed trugs-tools version differs from the version
under which the agent last read README.md and map/published.trl.
`language` is trugs_tools/data/language.trug.json in the installed package.
`sentence` is the instruction being authored; `graph` is its compiled TRUGS graph.

```trl
AGENT agent SHALL READ FILE entry.
AGENT agent SHALL READ FILE primer ONCE.
AGENT agent SHALL READ FILE map SUBJECT_TO DATA version_changed
  THEN READ FILE entry.
AGENT agent SHALL READ FILE language THEN WRITE RECORD sentence.
AGENT agent SHALL VALIDATE RECORD graph.
```

Use TRL when communicating instructions; store and validate the graph as JSON.
Read an example or skill when the task calls for it. Read the map when a question
concerns another repository. The version directive is a reading rule; no background
version monitor or memory store is installed.

Dependency: trugs-tools `>=2.4.0,<3`.
Use trugs-agent check after placing these files. The self-check compiles hello,
validates, decompiles, recompiles, compares and checks placed instruction vocabulary.

Pointers: [logic graphs](https://github.com/TRUGS-LLC/TRUGS-AGENT/tree/main/examples/logic-graph),
[folder mapping](https://github.com/TRUGS-LLC/TRUGS-AGENT/tree/main/examples/map-a-folder),
[calculator](https://github.com/TRUGS-LLC/TRUGS-ACCOUNTING-CALCULATOR),
[web graphs](https://github.com/TRUGS-LLC/TRUGS-WEB),
[language](https://github.com/TRUGS-LLC/TRUGS), and the coming TRUGS-LAW repository.

Vocabulary: 233 words across 9 parts of speech (from the installed language file).

| Part of speech | Group | Words |
|---|---|---|
| noun (26) | actors | PROCESS SERVICE FUNCTION TRANSFORM PARTY AGENT PRINCIPAL |
| noun (26) | artifacts | DATA FILE RECORD MESSAGE STREAM RESOURCE INSTRUMENT |
| noun (26) | containers | PIPELINE STAGE MODULE NAMESPACE |
| noun (26) | boundaries | ENTRY EXIT INTERFACE ENDPOINT JURISDICTION |
| noun (26) | outcomes | ERROR EXCEPTION REMEDY |
| verb (80) | transform | FILTER EXCLUDE MAP SORT MERGE SPLIT FLATTEN AGGREGATE GROUP RENAME BATCH DISTINCT TAKE SKIP APPLY DERIVE UPDATE |
| verb (80) | move | READ WRITE SEND RECEIVE RETURN REQUEST RESPOND AUTHENTICATE DELIVER ASSIGN LOAD POST EMIT PRODUCE APPEND DELEGATE |
| verb (80) | obligate | VALIDATE ASSERT REQUIRE SHALL ASSERT_NOT INVARIANT |
| verb (80) | permit | ALLOW APPROVE GRANT OVERRIDE MAY ACCEPT SUGGEST |
| verb (80) | prohibit | DENY REJECT SHALL_NOT REVOKE |
| verb (80) | control | BRANCH MATCH RETRY TIMEOUT THROW EXISTS EXPIRE EQUALS EXCEEDS PRECEDES EXECUTE INVOKE HALT COMPLETE PASS |
| verb (80) | bind | DEFINE DECLARE IMPLEMENT NEST AUGMENT REPLACE CITE ADMINISTER STIPULATE HAVE |
| verb (80) | resolve | CATCH HANDLE RECOVER CURE INDEMNIFY |
| adjective (39) | type | STRING INTEGER BOOLEAN ARRAY OBJECT |
| adjective (39) | access | PUBLIC PRIVATE PROTECTED READONLY CONFIDENTIAL |
| adjective (39) | state | VALID INVALID NULL EMPTY PENDING ACTIVE FAILED MUTABLE IMMUTABLE BINDING VOID ENFORCEABLE EXPIRED PRECEDENT |
| adjective (39) | quantity | REQUIRED OPTIONAL UNIQUE MULTIPLE SOLE JOINT ONLY AT_LEAST EXACTLY |
| adjective (39) | priority | DEFAULT CRITICAL HIGH LOW MATERIAL SUBORDINATE |
| adverb (19) | timing | ASYNC SYNC SEQUENTIAL PARALLEL IMMEDIATE LAZY PROMPTLY FORTHWITH WITHIN |
| adverb (19) | repetition | ONCE ALWAYS NEVER BOUNDED |
| adverb (19) | degree | STRICTLY PARTIALLY SUBSTANTIALLY REASONABLY |
| adverb (19) | condition | UNCONDITIONALLY CONDITIONALLY |
| preposition (18) | flow | FEEDS ROUTES TO FROM RETURNS_TO |
| preposition (18) | dependency | BINDS DEPENDS_ON IMPLEMENTS EXTENDS SUBJECT_TO |
| preposition (18) | containment | CONTAINS |
| preposition (18) | reference | REFERENCES |
| preposition (18) | replacement | SUPERSEDES |
| preposition (18) | authority | GOVERNS PURSUANT_TO ON_BEHALF_OF |
| preposition (18) | binding | AS BY |
| conjunction (13) | sequence | THEN FINALLY |
| conjunction (13) | parallel | AND |
| conjunction (13) | alternative | OR ELSE |
| conjunction (13) | cause | IF WHEN WHILE |
| conjunction (13) | exception | UNLESS EXCEPT NOTWITHSTANDING PROVIDED_THAT WHEREAS |
| article (10) | specific | THE THIS |
| article (10) | universal | ALL EACH EVERY |
| article (10) | existential | ANY SOME A |
| article (10) | negative | NO NONE |
| pronoun (7) | self | SELF |
| pronoun (7) | result | RESULT OUTPUT |
| pronoun (7) | source | INPUT SOURCE |
| pronoun (7) | target | TARGET |
| pronoun (7) | legal_reference | SAID |
| level_prefix (21) | macro | YOTTA ZETTA EXA PETA TERA GIGA MEGA KILO HECTO DEKA |
| level_prefix (21) | default | BASE |
| level_prefix (21) | micro | DECI CENTI MILLI MICRO NANO PICO FEMTO ATTO ZEPTO YOCTO |
