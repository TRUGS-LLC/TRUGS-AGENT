#!/usr/bin/env python3
"""graph_equiv.py — structural-graph equivalence checker for localized editions.

The human-language-universality claim: because meaning in TRUGS lives in the
language-neutral graph (ids, types, parent_id, edges), an exhibit translated into another
human language must compile to the SAME structural graph as its source. The ONLY permitted
delta between editions is the human-readable property *values* (a node's `name`, `summary`,
`description`, …). Everything that carries meaning — node ids, types, hierarchy, the
canonical TRL keywords in `operation`/`modal`/`relation`/adjective slots, and the edge set —
must be byte-for-byte identical after normalisation.

This turns localization fidelity from an act of trust into a CI check (Fork A: prose
translates, TRL keywords stay canonical).

USAGE
    python3 tools/graph_equiv.py <source> <edition>

    Each argument is a directory (the single top-level *.trug.json in it is used) or a
    .trug.json file directly. Example (SC-8 contract — source dir, then one edition dir):

        python3 tools/graph_equiv.py examples/hello examples/hello

EXIT
    0  structurally identical (a faithful localization)
    1  structural mismatch (the editions disagree on meaning, not just wording)
    2  usage / IO error
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Property keys whose VALUES are human-readable prose and may differ between editions.
# Everything else (operation, modal, verb_subcategory, state, priority, timing, condition,
# access, type_hint, …) is a canonical TRL token and must match.
LOCALIZABLE = {
    "name",
    "summary",
    "description",
    "purpose",
    "title",
    "label",
    "text",
    "comment",
}


def _resolve(arg: str) -> Path:
    p = Path(arg)
    if p.is_dir():
        # Non-recursive: the source dir may itself contain edition subdirs.
        candidates = sorted(p.glob("*.trug.json"))
        if not candidates:
            raise FileNotFoundError(f"no *.trug.json directly in directory: {arg}")
        if len(candidates) > 1:
            raise ValueError(
                f"ambiguous: {len(candidates)} *.trug.json in {arg}: {[c.name for c in candidates]}"
            )
        return candidates[0]
    if p.is_file():
        return p
    raise FileNotFoundError(f"not found: {arg}")


def _strip(props: dict) -> dict:
    """Drop localizable prose; keep canonical TRL tokens, sorted for stable comparison."""
    return {k: props[k] for k in sorted(props) if k not in LOCALIZABLE}


def _structure(graph: dict) -> dict:
    """Project a graph onto its language-neutral structure (order-independent)."""
    nodes = {}
    for n in graph.get("nodes", []):
        nodes[n["id"]] = {
            "type": n.get("type"),
            "parent_id": n.get("parent_id"),
            "contains": sorted(n.get("contains", [])),
            "metric_level": n.get("metric_level"),
            "dimension": n.get("dimension"),
            "properties": _strip(n.get("properties", {})),
        }
    edges = sorted(
        (e.get("from_id"), e.get("to_id"), e.get("relation"))
        for e in graph.get("edges", [])
    )
    return {"nodes": nodes, "edges": edges}


def _diff(a: dict, b: dict) -> list[str]:
    out = []
    an, bn = a["nodes"], b["nodes"]
    for nid in sorted(set(an) | set(bn)):
        if nid not in an:
            out.append(f"  node only in edition: {nid}")
        elif nid not in bn:
            out.append(f"  node only in source : {nid}")
        elif an[nid] != bn[nid]:
            out.append(f"  node differs structurally: {nid}")
            for k in sorted(set(an[nid]) | set(bn[nid])):
                if an[nid].get(k) != bn[nid].get(k):
                    out.append(
                        f"      {k}: source={an[nid].get(k)!r} edition={bn[nid].get(k)!r}"
                    )
    if a["edges"] != b["edges"]:
        sa, sb = set(a["edges"]), set(b["edges"])
        for e in sorted(sa - sb):
            out.append(f"  edge only in source : {e}")
        for e in sorted(sb - sa):
            out.append(f"  edge only in edition: {e}")
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        src_path, ed_path = _resolve(argv[1]), _resolve(argv[2])
        src = json.loads(src_path.read_text(encoding="utf-8"))
        ed = json.loads(ed_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"graph_equiv: ERROR: {exc}", file=sys.stderr)
        return 2

    diffs = _diff(_structure(src), _structure(ed))
    if diffs:
        print(
            f"graph_equiv: FAIL — {src_path} and {ed_path} are NOT structurally equivalent:"
        )
        print("\n".join(diffs))
        return 1
    print(
        f"graph_equiv: PASS — {ed_path.parent.name or ed_path.name} is a faithful localization "
        f"(same structural graph as {src_path.parent.name or src_path.name})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
