"""Parts of the one offline kit checker."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from kit_check import language, run, trl_check


def layout(root):
    required = [
        "README.md",
        "PRIMER.md",
        "AGENTS.md",
        "map/published.trl",
        "map/published.trug.json",
        "map/repositories.json",
        "map/README.md",
        "kit/source.md",
        "kit/primer.md.in",
        "kit/AGENTS.md",
        "kit/CLAUDE.md",
        "kit/.cursor/rules/trugs-agent.mdc",
        "kit/.claude-plugin/plugin.json",
        "installer/pyproject.toml",
        "installer/src/trugs_agent/cli.py",
        "installer/tests/test_installer.py",
        "eval/items.json",
        "eval/README.md",
        "tools/graph_equiv.py",
        "CONTRIBUTING.md",
        "LICENSE",
        "NOTICE",
        "CHANGELOG.md",
        "SECURITY.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/ISSUE_TEMPLATE/config.yml",
    ]
    for name in (
        "hello",
        "todo-app",
        "logic-graph",
        "refactor_a_program",
        "skill_refactor_safely",
        "skill_ship_safely",
        "map-a-folder",
        "calculator",
    ):
        required += [
            f"examples/{name}/README.md",
            f"examples/{name}/check.sh",
            f"examples/{name}/{name}.trl",
        ]
    for name in (
        "write-trl",
        "validate",
        "compile-decompile",
        "fix-by-rule",
        "map-a-folder",
        "run-calculator",
    ):
        required.append(f"kit/skills/{name}/SKILL.md")
    for name in required:
        if not (root / name).is_file():
            raise ValueError("missing kit path: " + name)
    primer = (root / "kit/primer.md.in").read_text()
    for section in (
        "TRL/TRUGS in one screen",
        "Vocabulary",
        "Grammar essentials",
        "Sentence → graph compilation",
        "Validation",
        "Authoring checklist",
        "References",
    ):
        if not re.search(r"^## " + re.escape(section), primer, re.MULTILINE):
            raise ValueError("missing primer section: " + section)


def file_list(root):
    # The release tree has no generated caches or build outputs.
    ignored = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        "build",
        "dist",
    }
    if (root / ".git").exists():
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=root,
            capture_output=True,
            check=True,
        )
        return sorted(
            {Path(name.decode()) for name in result.stdout.split(b"\0") if name},
            key=lambda p: p.as_posix().encode(),
        )
    result = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(
            part in ignored or part.endswith(".egg-info") for part in relative.parts
        ):
            continue
        if path.is_file():
            result.append(relative)
    return sorted(result, key=lambda p: p.as_posix().encode())


def examples(root, scratch, write):
    for path in sorted((root / "examples").glob("*/*.trl")):
        expected = run(["trug", "trl", "compile", str(path)])
        graph = path.with_suffix(".trug.json")
        if write:
            graph.write_text(expected)
        elif not graph.exists() or graph.read_bytes() != expected.encode():
            raise ValueError(f"lesson graph drift: {path.relative_to(root)}")
        run(["trug", "validate", str(graph)])
        canonical = run(["trug", "trl", "decompile", str(graph)])
        returned = scratch / "returned.trug.json"
        returned.write_text(run(["trug", "trl", "compile", "-"], data=canonical))
        run(
            [
                sys.executable,
                str(root / "tools/graph_equiv.py"),
                str(graph),
                str(returned),
            ]
        )
    # Source annotations in the reused program are executable contracts too.
    app = (root / "examples/todo-app/app.py").read_text()
    for block in re.findall(r"<trl>(.*?)</trl>", app, re.S):
        trl_check(re.sub(r"(?m)^# ?", "", block), "todo annotations", scratch)


def maps(root, scratch, write, repositories=None):
    source = root / "map/published.trl"
    expected = run(["trug", "trl", "compile", str(source)])
    graph = root / "map/published.trug.json"
    if write:
        graph.write_text(expected)
    elif not graph.is_file() or graph.read_bytes() != expected.encode():
        raise ValueError("published graph drift")
    run(["trug", "validate", str(graph)])
    canonical = run(["trug", "trl", "decompile", str(graph)])
    returned = scratch / "published-back.trug.json"
    returned.write_text(run(["trug", "trl", "compile", "-"], data=canonical))
    run([sys.executable, str(root / "tools/graph_equiv.py"), str(graph), str(returned)])
    records = json.loads((root / "map/repositories.json").read_text())
    required = {
        "TRUGS": ("37bb78c7", "live_specification"),
        "TRUGS-TOOLS": ("a0a4218f", "live_language_tools"),
        "TRUGS-STORE": ("08c4bdec", "live_graph_storage"),
        "TRUGS-ACCOUNTING-CALCULATOR": ("b806f115", "live_compute"),
        "TRUGS-SITE": ("d2de19cb", "live_specification_site"),
        "TRUGS-WEB": ("d7db95df080155af59b506b11740d33afa4f9c93", "candidate_describe"),
        "TRUGS-VIEWER": ("60117feb", "demonstration"),
        "TRUGS-TRL": (None, "coming_language"),
        "TRUGS-LAW": (None, "coming_law"),
        "TRUGS-AGENT": (None, "candidate_onboarding"),
    }
    if len(records) != len(required) or {r["repository"] for r in records} != set(
        required
    ):
        raise ValueError("repository map membership differs")
    readme = (root / "map/README.md").read_text()
    sentences = []
    for row in records:
        repo = row["repository"]
        if (row["revision"], row["group"]) != required[repo]:
            raise ValueError("repository group/revision differs: " + repo)
        if not row["installation"] or not row["role"]:
            raise ValueError("missing repository binding: " + repo)
        if repo in ("TRUGS-TRL", "TRUGS-LAW") and (
            row["instructions"] is not None
            or row["role"] != "Say; coming, with no date"
        ):
            raise ValueError("coming repository binding differs")
        if (
            repo == "TRUGS-VIEWER"
            and row["role"] != "Describe; a demonstration, not in active development"
        ):
            raise ValueError("viewer status differs")
        for value in (row["resource"], row["group"], row["role"], row["installation"]):
            if value not in readme:
                raise ValueError("map README binding differs: " + repo)
        sentences.append(
            f"AGENT reader SHALL READ RESOURCE {row['resource']} SUBJECT_TO DATA {row['group']}."
        )
        if repositories and repo not in (
            "TRUGS-WEB",
            "TRUGS-VIEWER",
            "TRUGS-TRL",
            "TRUGS-LAW",
            "TRUGS-AGENT",
        ):
            actual = run(
                ["git", "-C", str(Path(repositories) / repo), "rev-parse", "HEAD"]
            ).strip()
            if not actual.startswith(row["revision"]):
                raise ValueError("source revision differs: " + repo)
    if source.read_text() != "\n\n".join(sentences) + "\n":
        raise ValueError("published TRL differs from repository bindings")
    copied = scratch / "index-input"
    copied.mkdir()
    for relative in file_list(root):
        if relative == Path("folder.trug.json"):
            continue
        destination = copied / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / relative, destination)
    index = run(["trugs-web", "map", str(copied), "--include-hidden"])
    generated = scratch / "index.trug.json"
    generated.write_text(index)
    run(["trug", "validate", str(generated)])
    if write:
        (root / "folder.trug.json").write_text(index)
    elif (
        not (root / "folder.trug.json").is_file()
        or (root / "folder.trug.json").read_bytes() != index.encode()
    ):
        raise ValueError(
            "repository index differs; regenerate with the installed trugs-web"
        )


def commands(root, scratch, repositories=None, calculator_source=None):
    candidates = [root / "README.md", root / "PRIMER.md"]
    candidates += sorted((root / "kit/skills").rglob("*.md"))
    candidates += sorted((root / "examples").rglob("*.md"))
    count = 0
    seen = set()
    pattern = re.compile(r"```sh\n(.*?)\n```\n<!-- expect: (.*?) -->", re.S)
    for path in candidates:
        text = path.read_text()
        entries = pattern.findall(text)
        if len(entries) != len(re.findall(r"^```sh$", text, re.M)):
            raise ValueError(
                "command lacks expected result: " + str(path.relative_to(root))
            )
        for command, expected in entries:
            expected = json.loads(expected)
            # Prepared repositories are an explicit input to the calculator lesson.
            args = ["bash", "-c", command]
            if "examples/calculator/check.sh" in command and repositories:
                args = [
                    "bash",
                    "examples/calculator/check.sh",
                    "--repositories",
                    str(repositories),
                ]
            if "examples/calculator/check.sh" in command and calculator_source:
                args += ["--calculator-source", str(calculator_source)]
            if command not in seen:
                result = subprocess.run(args, cwd=root, text=True, capture_output=True)
                if (
                    result.returncode != expected["status"]
                    or result.stdout != expected["stdout"]
                ):
                    raise ValueError(
                        f"command differs: {command}\n{result.stdout}{result.stderr}"
                    )
                seen.add(command)
            count += 1
    for script in (root / "examples").glob("*/check.sh"):
        if f"bash {script.relative_to(root).as_posix()}" not in seen:
            raise ValueError("unchecked example: " + script.parent.name)
    run([sys.executable, str(root / "tools/lesson.py"), "install"])
    print(f"PASS: command_check ({count} stated commands, {len(seen)} distinct)")


def eval_sources(root, scratch, repositories=None):
    records = json.loads((root / "eval/items.json").read_text())
    if not records:
        raise ValueError("no fixed evaluation items")
    for row in records:
        source = row["source"]
        if not row["prompt"] or not row["answer"] or not source.get("evidence"):
            raise ValueError("evaluation item lacks source")
        if source["kind"] == "help":
            command = source["command"]
            if command[0] not in ("trug", "trugs-web") or command[-1] != "--help":
                raise ValueError("unsupported evaluation help source")
            text = " ".join(run(command).split())
            if not all(phrase in text for phrase in source["evidence"]):
                raise ValueError("evaluation answer absent from help: " + row["id"])
        elif source["kind"] == "language":
            word = next(w for w in language() if w["word"] == source["word"])
            if any(word.get(key) != value for key, value in source["evidence"].items()):
                raise ValueError("evaluation answer absent from language file")
        elif source["kind"] == "trugs_readme":
            if not repositories:
                raise ValueError("README source check needs --repositories")
            text = (Path(repositories) / "TRUGS/README.md").read_text()
            if not all(phrase in text for phrase in source["evidence"]):
                raise ValueError("evaluation answer absent from TRUGS README")
        else:
            raise ValueError("unsupported evaluation source")
        if source["kind"] == "language":
            text = json.dumps(word)
        answers = row["answer"] if isinstance(row["answer"], list) else [row["answer"]]
        normalized = " ".join(text.split())
        if not all(answer in normalized for answer in answers):
            raise ValueError("evaluation expected answer not in its cited source")

    print("PASS: fixed source citations (no evaluation run)")


def hygiene(root):
    patterns = [
        "/" + "home" + "/",
        "/" + "Users" + "/",
        r"\bOD\d{4}\b",
        r'https?://[^\s"<>]*-dev\b',
        r"https?://github[.]com/(?!TRUGS-LLC/)[^\s]+",
        r"\b" + "la" + "ne" + r"\b",
        r"\bcore_v1[.]0[.]0\b",
        "TRUG[/]L",
        "trugs-" + "folder",
        "trug-a-" + "folder",
        r"(?<![\w])" + "t" + r"g(?![\w])",
    ]
    for relative in file_list(root):
        path = root / relative
        if path.is_symlink():
            raise ValueError("candidate symlink: " + str(relative))
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        if any(re.search(pattern, text) for pattern in patterns):
            raise ValueError("retired or nonpublic reference: " + str(relative))
        process_word = "au" + "dit"
        clean = text.replace("trug " + process_word, "").replace(
            "corpus " + process_word, ""
        )
        if re.search(r"\b" + process_word + r"\b", clean, re.IGNORECASE):
            raise ValueError("nonpublic process reference: " + str(relative))
    workflows = list((root / ".github/workflows").glob("*"))
    if len(workflows) != 1:
        raise ValueError("expected one workflow")
    workflow = workflows[0].read_text()
    if "kit_check.py" not in workflow or "installer/tests" not in workflow:
        raise ValueError("workflow lacks required checks")
    if hashlib.sha256((root / "LICENSE").read_bytes()).hexdigest() != LICENSE_DIGEST:
        raise ValueError("Apache licence changed")


LICENSE_DIGEST = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
