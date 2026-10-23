"""Parts of the one offline kit checker."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from kit_check import language, run, trl_check
from trugs_agent.markdown import tokens


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
    records = json.loads((root / "map/repositories.json").read_text())
    sentences = [
        f"AGENT reader SHALL READ RESOURCE {row['resource']} SUBJECT_TO DATA {row['group']}."
        for row in records
    ]
    if write:
        source.write_text("\n\n".join(sentences) + "\n")
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
    required = {
        "TRUGS": ("37bb78c7", "live_specification"),
        "TRUGS-TOOLS": ("a0a4218f", "live_language_tools"),
        "TRUGS-STORE": ("f363268b", "live_graph_storage"),
        "TRUGS-ACCOUNTING-CALCULATOR": ("b806f115", "live_compute"),
        "TRUGS-SITE": ("d2de19cb", "live_specification_site"),
        "TRUGS-WEB": ("9b6cd1f60e1deaa03073f89c78f1f6d5ae277e28", "live_describe"),
        "TRUGS-VIEWER": ("c27e39fe", "demonstration"),
        "TRUGS-TRL": (None, "coming_language"),
        "TRUGS-LAW": (None, "coming_law"),
        "TRUGS-AGENT": (None, "live_onboarding"),
    }
    if len(records) != len(required) or {r["repository"] for r in records} != set(
        required
    ):
        raise ValueError("repository map membership differs")
    readme = (root / "map/README.md").read_text()
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
        if (
            repo == "TRUGS-VIEWER"
            and "https://trugs-llc.github.io/TRUGS-VIEWER/" not in row["installation"]
        ):
            raise ValueError("viewer address differs")
        for value in (row["resource"], row["group"], row["role"], row["installation"]):
            if value not in readme:
                raise ValueError("map README binding differs: " + repo)
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


def command_environment(root, scratch, wheelhouse):
    """Resolve printed index installs using local wheels and a scratch-built kit."""
    import venv

    wheelhouse = Path(wheelhouse or Path(sys.prefix).parent / "wheelhouse").resolve()
    if not wheelhouse.is_dir():
        raise ValueError("command check needs a prepared --wheelhouse")
    source = scratch / "command-installer"
    shutil.copytree(root / "installer", source)
    wheels = scratch / "command-wheels"
    run(
        [
            sys.executable,
            "-m",
            "build",
            "--no-isolation",
            "--wheel",
            "--outdir",
            str(wheels),
            str(source),
        ]
    )
    # Only the wheel just built may satisfy trugs-agent, even if an input bundle
    # also contains an older wheel with that same version.
    for wheel in wheelhouse.glob("*.whl"):
        if not wheel.name.lower().startswith("trugs_agent-"):
            (wheels / wheel.name).symlink_to(wheel)
    environment = scratch / "command-venv"
    venv.EnvBuilder(with_pip=True).create(environment)
    env = os.environ.copy()
    env.update(
        PATH=str(environment / "bin") + os.pathsep + env.get("PATH", ""),
        PIP_NO_INDEX="1",
        PIP_FIND_LINKS=wheels.as_uri(),
        PIP_NO_BUILD_ISOLATION="1",
        PIP_DISABLE_PIP_VERSION_CHECK="1",
        PIP_NO_CACHE_DIR="1",
        PIP_CONFIG_FILE=os.devnull,
    )
    result = subprocess.run(
        [
            str(environment / "bin/python"),
            "-m",
            "pip",
            "install",
            "--quiet",
            "--no-build-isolation",
            "build",
            "setuptools",
            "wheel",
        ],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(
            "offline command tools failed: " + result.stdout + result.stderr
        )
    return env


def commands(root, scratch, repositories=None, calculator_source=None, wheelhouse=None):
    candidates = [root / "README.md", root / "PRIMER.md"]
    candidates += sorted((root / "kit/skills").rglob("*.md"))
    candidates += sorted((root / "examples").rglob("*.md"))
    candidates += [
        root / relative
        for relative in file_list(root)
        if (relative.suffix.lower() == ".md" or relative.name.endswith(".md.in"))
        and root / relative not in candidates
    ]
    count = 0
    seen = {}
    checked_examples = set()
    # These are declared lesson inputs, not substitutions for the printed command.
    env = (
        command_environment(root, scratch, wheelhouse)
        if (root / "installer/pyproject.toml").is_file()
        else os.environ.copy()
    )
    env["repositories"] = str(Path(repositories).resolve()) if repositories else ""
    env["calculator_source"] = (
        str(Path(calculator_source).resolve()) if calculator_source else ""
    )
    for path in candidates:
        try:
            parsed = tokens(path.read_text())
        except ValueError as exc:
            raise ValueError(f"{path.relative_to(root)}: {exc}") from exc
        for index, token in enumerate(parsed):
            if token.type != "fence":
                continue
            info = token.info.split()
            if not info or info[0] not in ("sh", "bash", "shell"):
                continue
            command = token.content
            location = f"{path.relative_to(root)}:{token.map[0] + 2}"
            following = parsed[index + 1] if index + 1 < len(parsed) else None
            expectation = None
            if (
                following is not None
                and following.type == "html_block"
                and following.level == token.level
            ):
                expectation = re.fullmatch(
                    r"<!-- expect: (.*?) -->\s*", following.content, re.DOTALL
                )
            if expectation is None:
                raise ValueError(f"command lacks expected result at {location}")
            try:
                expected = json.loads(expectation[1])
            except ValueError as exc:
                raise ValueError(
                    f"invalid command expectation at {location}: {exc}"
                ) from exc
            if (
                not isinstance(expected, dict)
                or type(expected.get("status")) is not int
                or not isinstance(expected.get("stdout"), str)
            ):
                raise ValueError(
                    f"invalid command expectation at {location}: {expected!r}"
                )
            if command not in seen:
                result = subprocess.run(
                    ["bash", "-c", command],
                    cwd=root,
                    env=env,
                    text=True,
                    capture_output=True,
                )
                seen[command] = result, location
            result, first_location = seen[command]
            # Execution may be shared; every occurrence still owes a comparison.
            if (
                result.returncode != expected["status"]
                or result.stdout != expected["stdout"]
            ):
                repeated = (
                    f"; contradictory expectations, first stated at {first_location}"
                    if first_location != location
                    else ""
                )
                raise ValueError(
                    f"command differs at {location}{repeated}: {command}\n"
                    f"expected: {expected!r}\n"
                    f"actual status: {result.returncode}, stdout: {result.stdout!r}\n"
                    f"{result.stderr}"
                )
            words = shlex.split(command)
            if len(words) >= 2 and words[0] == "bash":
                checked_examples.add(words[1])
            count += 1
    for script in (root / "examples").glob("*/check.sh"):
        if script.relative_to(root).as_posix() not in checked_examples:
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
