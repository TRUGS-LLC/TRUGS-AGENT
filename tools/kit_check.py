#!/usr/bin/env python3
"""Offline kit entry point. All generated content is checked before lessons run."""

from __future__ import annotations

import argparse
import importlib.resources
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "installer/src"))
from trugs_agent.markdown import blocks  # noqa: E402


def run(args, *, cwd=ROOT, data=None):
    result = subprocess.run(args, cwd=cwd, input=data, text=True, capture_output=True)
    if result.returncode:
        raise ValueError(
            f"{args[0]} failed ({result.returncode}): {result.stdout}{result.stderr}"
        )
    return result.stdout


def language():
    graph = json.loads(
        importlib.resources.files("trugs_tools")
        .joinpath("data/language.trug.json")
        .read_text()
    )
    return [
        node["properties"] for node in graph["nodes"] if "word" in node["properties"]
    ]


def vocabulary():
    words = language()
    groups = {}
    for word in words:
        groups.setdefault(word["speech"], {}).setdefault(
            word.get("subcategory", ""), []
        ).append(word["word"])
    lines = [
        f"Vocabulary: {len(words)} words across {len(groups)} parts of speech (from the installed language file).",
        "",
        "| Part of speech | Group | Words |",
        "|---|---|---|",
    ]
    for speech, subs in groups.items():
        count = sum(map(len, subs.values()))
        for sub, values in subs.items():
            lines.append(f"| {speech} ({count}) | {sub} | {' '.join(values)} |")
    return "\n".join(lines)


def generated():
    source = (ROOT / "kit/source.md").read_text()
    text = "<!-- Generated from kit/source.md; edit the source. -->\n" + source.replace(
        "{{VOCABULARY}}", vocabulary()
    )
    outputs = {name: text for name in ("AGENTS.md", "kit/AGENTS.md", "kit/CLAUDE.md")}
    outputs["kit/.cursor/rules/trugs-agent.mdc"] = (
        "---\ndescription: TRUGS onboarding\nalwaysApply: true\n---\n\n" + text
    )
    outputs["kit/.claude-plugin/plugin.json"] = (
        json.dumps(
            {
                "name": "trugs-agent",
                "version": "2.0.0",
                "description": text,
                "author": {"name": "TRUGS LLC"},
                "homepage": "https://github.com/TRUGS-LLC/TRUGS-AGENT",
                "repository": "https://github.com/TRUGS-LLC/TRUGS-AGENT",
                "license": "Apache-2.0",
            },
            indent=2,
        )
        + "\n"
    )
    primer = (
        (ROOT / "kit/primer.md.in").read_text().replace("{{VOCABULARY}}", vocabulary())
    )
    outputs["PRIMER.md"] = primer
    outputs["installer/LICENSE"] = (ROOT / "LICENSE").read_text()
    outputs["installer/NOTICE"] = (ROOT / "NOTICE").read_text()
    for name in list(outputs):
        if name.startswith("kit/") and name != "kit/source.md":
            outputs["installer/src/trugs_agent/payload/" + name[4:]] = outputs[name]
    requirement = re.search(r"trugs-tools `(>=\S+)`", source)[1]
    template = (ROOT / "installer/pyproject.toml.in").read_text()
    outputs["installer/pyproject.toml"] = template.replace(
        "{{TOOLS_REQUIREMENT}}", requirement
    )
    return outputs


def forms(write=False):
    for name, expected in generated().items():
        path = ROOT / name
        if write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected)
        elif not path.is_file() or path.read_bytes() != expected.encode():
            raise ValueError(f"generated drift: {name}")


def trl_check(text, label, scratch):
    path = scratch / "block.trl"
    path.write_text(text)
    graph = run(["trug", "trl", "compile", str(path)])
    (scratch / "block.trug.json").write_text(graph)
    run(["trug", "validate", str(scratch / "block.trug.json")])
    # The tools vocabulary scanner reads tagged blocks. Adapt fences without changing tools.
    (scratch / "block.md").write_text("<trl>\n" + text + "</trl>\n")
    run("trug audit vocab".split() + [str(scratch / "block.md")])


def documents(scratch):
    from kit_parts import file_list

    for relative in file_list(ROOT):
        path = ROOT / relative
        if path.suffix.lower() == ".md" or path.name.endswith(".md.in"):
            text = path.read_text()
            try:
                for kind, body in blocks(text):
                    if kind == "trl":
                        trl_check(body, str(path), scratch)
            except ValueError as exc:
                raise ValueError(f"{relative}: {exc}") from exc
    for path in sorted((ROOT / "kit").rglob("*")):
        if path.suffix == ".mdc":
            for kind, body in blocks(path.read_text()):
                if kind == "trl":
                    trl_check(body, str(path), scratch)
    plugin = json.loads((ROOT / "kit/.claude-plugin/plugin.json").read_text())
    for kind, body in blocks(plugin["description"]):
        if kind == "trl":
            trl_check(body, "plugin", scratch)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repositories",
        type=Path,
        required=True,
        help="directory of prepared public repository checkouts",
    )
    parser.add_argument(
        "--calculator-source",
        type=Path,
        help="optional prepared calculator source copy",
    )
    parser.add_argument(
        "--wheelhouse",
        type=Path,
        default=Path(sys.prefix).parent / "wheelhouse",
        help="offline wheels (default: wheelhouse beside the active environment)",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="regenerate forms, lesson graphs and the repository index",
    )
    args = parser.parse_args()
    try:
        from kit_parts import layout

        layout(ROOT)
        forms(args.generate)
        with tempfile.TemporaryDirectory(prefix="kit-check-") as temp:
            scratch = Path(temp)
            documents(scratch)
            from kit_parts import commands, eval_sources, examples, hygiene, maps

            examples(ROOT, scratch, args.generate)
            maps(ROOT, scratch, args.generate, args.repositories)
            eval_sources(ROOT, scratch, args.repositories)
            hygiene(ROOT)
            commands(
                ROOT,
                scratch,
                args.repositories,
                args.calculator_source,
                args.wheelhouse,
            )
        print("PASS: kit_check")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
