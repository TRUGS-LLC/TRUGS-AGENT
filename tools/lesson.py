#!/usr/bin/env python3
"""Run a lesson and compare its promised result; writes only temporary outputs."""

from __future__ import annotations

import argparse
import json
import runpy
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import venv
from pathlib import Path

from kit_check import ROOT, run


def round_trip(source, graph, temp):
    actual = run(["trug", "trl", "compile", str(source)])
    if actual.encode() != graph.read_bytes():
        raise ValueError(f"compiled graph drift: {graph.name}")
    run(["trug", "validate", str(graph)])
    canonical = run(["trug", "trl", "decompile", str(graph)])
    back = run(["trug", "trl", "compile", "-"], data=canonical)
    returned = temp / "round-trip.trug.json"
    returned.write_text(back)
    run([sys.executable, str(ROOT / "tools/graph_equiv.py"), str(graph), str(returned)])


def calculator(repositories, temp, source_copy=None):
    if not repositories:
        raise ValueError(
            "calculator needs --repositories with the prepared public checkouts"
        )
    original = source_copy or Path(repositories) / "TRUGS-ACCOUNTING-CALCULATOR"
    source = temp / "calculator-source"
    # The caller supplies only the public calculator checkout.
    shutil.copytree(original, source, ignore=shutil.ignore_patterns(".git", "target"))
    target = temp / "target"
    run(
        [
            "cargo",
            "build",
            "--offline",
            "--locked",
            "--release",
            "--target-dir",
            str(target),
        ],
        cwd=source,
    )
    binary = target / "release/trugs-accounting-calculator"
    checked = json.loads(
        run([str(binary), "validate", "examples/invoice/invoice.trl"], cwd=source)
    )
    if checked != {"build_supported": True, "valid": True}:
        raise ValueError("calculator validation differs")
    # These are the calculator's documented build inputs, not captured process state.
    import os

    env = os.environ.copy()
    cargo_home = temp / "cargo-home"
    cargo_home.mkdir()
    env.update(CARGO_HOME=str(cargo_home), CARGO_TARGET_DIR=str(target))
    result = subprocess.run(
        [
            str(binary),
            "check",
            "examples/invoice/invoice.trug.json",
            "examples/invoice/CASES-visible.json",
            str(temp / "invoice-run"),
        ],
        cwd=source,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise ValueError("calculator check failed: " + result.stdout + result.stderr)
    expected = {
        "agreed": 6,
        "count": 6,
        "disagreeing_positions": [],
        "execution_failures": 0,
    }
    if json.loads(result.stdout) != expected:
        raise ValueError("calculator invoice counts differ")


def install_lesson(temp):
    source = temp / "installer"
    shutil.copytree(ROOT / "installer", source)
    wheels = temp / "wheels"
    run(
        [
            sys.executable,
            "-m",
            "build",
            "--no-isolation",
            "--outdir",
            str(wheels),
            "--wheel",
            str(source),
        ]
    )
    (wheel,) = wheels.glob("*.whl")
    environment = temp / "venv"
    venv.EnvBuilder(with_pip=True, system_site_packages=True).create(environment)
    python = environment / "bin/python"
    # Share the prepared interpreter's runtime dependencies even when it is a
    # virtual environment (system_site_packages alone only shares its base).
    purelib = Path(
        run(
            [
                str(python),
                "-c",
                "import sysconfig; print(sysconfig.get_path('purelib'))",
            ]
        ).strip()
    )
    (purelib / "prepared-runtime.pth").write_text(sysconfig.get_path("purelib") + "\n")
    run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--no-build-isolation",
            "--no-deps",
            "--ignore-installed",
            str(wheel),
        ]
    )
    project = temp / "project"
    project.mkdir()
    exe = environment / "bin/trugs-agent"
    # Use the newly installed CLI with its own dependency entry points.
    import os

    env = os.environ.copy()
    result = subprocess.run(
        [str(exe), "install", "--project", str(project)],
        text=True,
        capture_output=True,
        env=env,
    )
    if result.returncode or not result.stdout.endswith("PASS: trugs-agent check\n"):
        raise ValueError("installed candidate failed: " + result.stdout + result.stderr)
    result = subprocess.run(
        [str(exe), "check", "--project", str(project)],
        text=True,
        capture_output=True,
        env=env,
    )
    if result.returncode or result.stdout != "PASS: trugs-agent check\n":
        raise ValueError("installed check command failed")
    return wheel


def example(name, temp, repositories=None, calculator_source=None):
    path = ROOT / "examples" / name
    round_trip(path / (name + ".trl"), path / (name + ".trug.json"), temp)
    if name == "todo-app":
        result = run([sys.executable, str(path / "app.py")])
        expected = (
            "All todos:\n  [done] Learn TRL vocabulary\n  [pending] Add AGENTS.md to my project\n"
            "  [pending] Write TRL specifications\n\nPending:\n  [ ] Add AGENTS.md to my project\n"
            "  [ ] Write TRL specifications\n"
        )
        if result != expected:
            raise ValueError("todo program output differs")
        app = runpy.run_path(str(path / "app.py"))
        todos = []
        for invalid in ("", "  "):
            try:
                app["create_todo"](invalid, todos)
            except ValueError:
                pass
            else:
                raise ValueError("todo accepted an invalid title")
        item = app["create_todo"](" Task ", todos)
        assert item["title"] == "Task"
        app["complete_todo"](1, todos)
        assert app["list_todos"](todos, True) == [item]
        assert app["list_todos"](todos, False) == []
        try:
            app["complete_todo"](99, todos)
        except KeyError:
            pass
        else:
            raise ValueError("todo accepted a missing id")
    elif name == "map-a-folder":
        mapped = temp / "mapped.trug.json"
        mapped.write_text(run(["trugs-web", "map", str(path / "sample")]))
        run(["trug", "validate", str(mapped)])
        # A file map carries non-language metadata. Decompile and ensure the
        # resulting sentence compiles and validates; that metadata is not TRL.
        back = temp / "mapped-back.trug.json"
        back.write_text(
            run(
                ["trug", "trl", "compile", "-"],
                data=run(["trug", "trl", "decompile", str(mapped)]),
            )
        )
        run(["trug", "validate", str(back)])
    elif name == "calculator":
        calculator(repositories, temp, calculator_source)
    print(f"PASS: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson", choices=("example", "install", "validate", "fix"))
    parser.add_argument("name", nargs="?")
    parser.add_argument("--repositories", type=Path)
    parser.add_argument("--calculator-source", type=Path)
    args = parser.parse_args()
    try:
        with tempfile.TemporaryDirectory(prefix="kit-lesson-") as directory:
            temp = Path(directory)
            if args.lesson == "example":
                example(args.name, temp, args.repositories, args.calculator_source)
            elif args.lesson == "install":
                install_lesson(temp)
                print("PASS: install and self-check")
            elif args.lesson == "validate":
                run(["trug", "validate", str(ROOT / "examples/hello/hello.trug.json")])
                print("PASS: validate")
            elif args.lesson == "fix":
                result = subprocess.run(
                    ["trug", "trl", "compile", "-"],
                    input="PIPELINE bad SHALL VALIDATE.\n",
                    text=True,
                    capture_output=True,
                )
                if (
                    result.returncode != 1
                    or "CONSTRAINT_REQUIRES_ACTOR" not in result.stderr
                ):
                    raise ValueError("expected CONSTRAINT_REQUIRES_ACTOR rejection")
                run(
                    ["trug", "trl", "compile", "-"],
                    data="AGENT repaired SHALL VALIDATE.\n",
                )
                print("PASS: CONSTRAINT_REQUIRES_ACTOR fixed")
        return 0
    except (ValueError, OSError, AssertionError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
