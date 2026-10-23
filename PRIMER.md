# TRUGS primer — TRL and graph authoring

Read the entry screen first. This primer tracks the public
[language specification](https://github.com/TRUGS-LLC/TRUGS/tree/main/TRUGS_LANGUAGE).
The installed compiler is the check on examples, not an assertion of program behaviour.

## TRL/TRUGS in one screen

TRL is constrained English for communicating. TRUGS JSON stores typed nodes,
edges and hierarchy. Compilable source contracts round-trip through canonical
TRL; sugar, formatting and arbitrary JSON properties need not survive.

The root envelope:

```json
{"name":"lesson","version":"1.0.0","type":"PROJECT","dimension":"system",
 "dimensions":{"system":{"description":"lesson"}},"nodes":[],"edges":[]}
```

Every node carries `id`, `type`, `properties`, `parent_id`, `contains`,
`metric_level` and `dimension`. Declare every used dimension in `dimensions`.
An edge carries `from_id`, `to_id`, and `relation`. A metric level has the form
`BASE_SERVICE` or `CENTI_FUNCTION` with a recognised SI prefix.

Minimal sentence (binding: `system` is the validating party):

```trl
PARTY system VALIDATE.
```

Binding: `api` is the actor, `output` is the destination. The sequence and bounded
retry are graph structure, not an automatic runtime implementation.

```trl
PARTY api SHALL FILTER ALL ACTIVE RECORD
  THEN WRITE RESULT TO ENDPOINT output
  OR RETRY BOUNDED 3 WITHIN 60s.
```

Author, compile, validate, read the named rule on failure, fix and repeat.
Read the entry always, this primer once, an example when needed, and the map for
repository questions. No memory routing or development routine is installed.

## Vocabulary

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

### Nouns — become graph nodes

Actors bear obligations; Artifacts hold data; Containers organise it; Boundaries
name interfaces; Outcomes represent errors and remedies. Use the generated table
above to look up each category and word.

### Verbs — become operations

Transform, Move, Obligate, Permit, Prohibit, Control, Bind and Resolve are verb
groups. The generated table lists their installed membership.

### Modals — obligation, only on Actor subjects

SHALL requires, MAY permits, SHALL_NOT prohibits. These tokens also appear in
verb groups in the language file; the generated table follows that file's speech
classification rather than inventing a second counted category.

### Adjectives — become node properties

Stack quantity, priority, state, access, type before a noun.

### Adverbs — become operation properties

Timing, repetition, degree and condition qualify an operation.

### Prepositions — become graph edges

Flow, dependency, structure, authority and binding are separate from verbs.

### Conjunctions — connect clauses

Sequence, parallel, alternative, condition and exception clauses form structures.

### Articles — scope selectors

Specific, universal, existential and negative selectors limit what a clause names.

### Pronouns — back-references

A pronoun resolves within its sentence, not a previous sentence.

### Level prefixes — hierarchy markers in metric_level

The language file lists SI prefixes. A bare prefix on a line is a level directive
and compiles to nothing; a prefix used inside a value helps name a metric level.

### Sugar — compiles to nothing

A quoted lowercase token such as `'please` is readability sugar. It carries no
graph meaning. Do not assume formatting or sugar survives decompilation.

## Grammar essentials

```text
sentence := clause (CONJUNCTION clause)* "." | definition "."
clause := subject verb_phrase object_phrase*
subject := noun_phrase | PRONOUN
noun_phrase := [ARTICLE] [ADJECTIVE]* NOUN [identifier]
verb_phrase := [modal] VERB adverb_phrase*
object_phrase := prep_phrase | noun_phrase | PRONOUN
prep_phrase := PREPOSITION noun_list
```

Modals require Actor subjects. Containers can Transform and Control; artifacts
can be subjects only of supported boolean Control verbs. A negative selector and
SHALL_NOT cannot negate the same clause. Transform verbs act on artifacts;
Move, Permit, Prohibit and Resolve each have object compatibility rules.
Verbs and prepositions are separate: ADMINISTER/GOVERNS, NEST/CONTAINS,
CITE/REFERENCES, REQUIRE/DEPENDS_ON, REPLACE/SUPERSEDES and AUGMENT/EXTENDS.

**Leading-keyword directives.** The full specification describes leading ASSERT,
ASSERT_NOT and INVARIANT forms. Author only syntax the installed compiler accepts;
do not infer parser support from this abbreviated grammar. The valid examples here
use subject-first clauses, with ASSERT in verb position when needed.

## Sentence → graph compilation

| Sentence element | Graph element |
|---|---|
| NOUN and identifier | typed node |
| adjective | node property |
| article | quantifier |
| verb | operation node |
| modal | modal property |
| adverb | operation qualifier |
| preposition | edge relation |
| conjunction | sequence or conditional structure |
| pronoun | scoped reference |
| DEFINE | defined term |
| sugar or level directive | no semantic graph node |

The compiler produces validated graphs or fails. Decompilation returns canonical
compilable text for supported graphs; compare structure after recompilation.

## Validation — the CORE ruleset

The structural rules always apply:

1. Unique node identifiers.
2. Edge endpoints refer to existing nodes.
3. Parent and contains relationships agree.
4. Parent metric levels are not smaller than child levels.
5. Used dimensions are declared.
6. Required node and edge fields exist.
7. Fields have the correct JSON types.
8. Extension properties are declared.
9. Metric-level prefixes are recognised.

Graphs declaring `core_v2.0.0` also receive compositional checks:

10. Subject–operation compatibility.
11. Operation–object compatibility.
12. Modifier–entity compatibility.
13. Qualifier–operation compatibility.
14. Modals require Actor subjects.
15. No double negation.
16. Reference scope.

The invalid example lesson demonstrates a rule name and its correction:

```sh
python tools/lesson.py fix
```
<!-- expect: {"status": 0, "stdout": "PASS: CONSTRAINT_REQUIRES_ACTOR fixed\n"} -->

Expected stdout: `PASS: CONSTRAINT_REQUIRES_ACTOR fixed`; exit status 0.

## Authoring checklist (do this every time you write a TRUG)

1. Include the root envelope and declare dimensions.
2. Supply all core node fields and a real noun and metric prefix.
3. Supply edge fields with a real preposition.
4. Put obligations on Actors and avoid double negation.
5. Compile, validate, fix the named rule, repeat.
6. Put TRL in fenced blocks marked trl; compile each block and round-trip graphs.

```sh
bash examples/hello/check.sh
```
<!-- expect: {"status": 0, "stdout": "PASS: hello\n"} -->

Expected stdout: `PASS: hello`; exit status 0.

## References (canonical — read when you need depth)

[Vocabulary](https://github.com/TRUGS-LLC/TRUGS/blob/main/TRUGS_LANGUAGE/SPEC_vocabulary.md),
[grammar](https://github.com/TRUGS-LLC/TRUGS/blob/main/TRUGS_LANGUAGE/SPEC_grammar.md),
[examples](https://github.com/TRUGS-LLC/TRUGS/blob/main/TRUGS_LANGUAGE/SPEC_examples.md),
[language graph](https://github.com/TRUGS-LLC/TRUGS/blob/main/TRUGS_LANGUAGE/language.trug.json),
and [the entry](README.md).
