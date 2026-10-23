"""Place generated instructions within a project, then check their language."""

from __future__ import annotations

import argparse
import importlib.resources
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    ".cursor/rules/trugs-agent.mdc",
    ".claude-plugin/plugin.json",
)
HELLO = "PARTY hello VALIDATE.\n"


def execute(args, data=None):
    result = subprocess.run(args, input=data, text=True, capture_output=True)
    if result.returncode:
        raise ValueError(f"{args[0]} failed: {result.stdout}{result.stderr}")
    return result.stdout


@contextmanager
def project_fd(project):
    path = Path(project).absolute()
    if path != path.resolve():
        raise ValueError("project path contains a symlink")
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        yield fd
    finally:
        os.close(fd)


@contextmanager
def parent_fd(root, relative, create=False):
    fd = os.dup(root)
    parts = Path(relative).parts
    if Path(relative).is_absolute() or any(x in (".", "..") for x in parts):
        os.close(fd)
        raise ValueError("unsafe destination")
    try:
        for part in parts[:-1]:
            if create:
                try:
                    os.mkdir(part, dir_fd=fd)
                except FileExistsError:
                    pass
            next_fd = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd
            )
            os.close(fd)
            fd = next_fd
        yield fd, parts[-1]
    finally:
        os.close(fd)


def inspect(root, name):
    try:
        with parent_fd(root, name) as (fd, leaf):
            info = os.stat(leaf, dir_fd=fd, follow_symlinks=False)
            if not stat.S_ISREG(info.st_mode):
                raise ValueError(f"not a regular destination: {name}")
            return (info.st_dev, info.st_ino, info.st_mtime_ns, info.st_size)
    except FileNotFoundError:
        return None


def read_placed(root, name):
    with parent_fd(root, name) as (fd, leaf):
        child = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        try:
            if not stat.S_ISREG(os.fstat(child).st_mode):
                raise ValueError(f"not a regular file: {name}")
            with os.fdopen(child, "r", encoding="utf-8", closefd=False) as stream:
                return stream.read()
        finally:
            os.close(child)


def fenced(text):
    opened = None
    kind = ""
    body = []
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if opened:
            if (
                match
                and match[1][0] == opened[0]
                and len(match[1]) >= len(opened)
                and not match[2].strip()
            ):
                if kind == "trl":
                    yield "\n".join(body) + "\n"
                opened, body = None, []
            else:
                body.append(line)
        elif match:
            opened, kind = match[1], match[2].strip().split(" ")[0]
    if opened:
        raise ValueError("unclosed instruction fence")


def checked_trl(text, temp):
    graph = execute(["trug", "trl", "compile", "-"], text)
    path = temp / "graph.trug.json"
    path.write_text(graph)
    execute(["trug", "validate", str(path)])
    vocab = temp / "vocabulary.md"
    vocab.write_text("<trl>\n" + text + "</trl>\n")
    execute("trug audit vocab".split() + [str(vocab)])
    return graph


def structure(graph):
    localizable = {
        "name",
        "summary",
        "description",
        "purpose",
        "title",
        "label",
        "text",
        "comment",
    }
    obj = json.loads(graph)
    nodes = {
        n["id"]: {
            **{k: n.get(k) for k in ("type", "parent_id", "metric_level", "dimension")},
            "contains": sorted(n.get("contains", [])),
            "properties": {
                k: v for k, v in n["properties"].items() if k not in localizable
            },
        }
        for n in obj["nodes"]
    }
    edges = sorted((e["from_id"], e["to_id"], e["relation"]) for e in obj["edges"])
    return nodes, edges


def check(project, quiet=False):
    with (
        project_fd(project) as root,
        tempfile.TemporaryDirectory(prefix="trugs-agent-check-") as directory,
    ):
        temp = Path(directory)
        graph = checked_trl(HELLO, temp)
        canonical = execute(["trug", "trl", "decompile", "-"], graph)
        compiled = checked_trl(canonical, temp)
        if structure(graph) != structure(compiled):
            raise ValueError("hello round trip differs")
        for name in FILES:
            text = read_placed(root, name)
            if name.endswith(".json"):
                text = json.loads(text)["description"]
            instruction_blocks = list(fenced(text))
            if not instruction_blocks:
                raise ValueError(f"no TRL instructions: {name}")
            for block in instruction_blocks:
                checked_trl(block, temp)
    if not quiet:
        print("PASS: trugs-agent check")


def install(project):
    # Report the complete declaration before opening any destination for writing.
    print("Files to place:", flush=True)
    for name in FILES:
        print(f"  {name}", flush=True)
    with project_fd(project) as root:
        before = {name: inspect(root, name) for name in FILES}
        existing = [name for name, info in before.items() if info is not None]
        if existing:
            if not sys.stdin.isatty():
                raise ValueError(
                    "existing files require terminal consent; nothing written"
                )
            print("Replace existing files: " + ", ".join(existing), flush=True)
            try:
                answer = input("Type yes to replace: ")
            except EOFError:
                answer = ""
            if answer.strip().lower() != "yes":
                raise ValueError("replacement declined; nothing written")
        payload = importlib.resources.files("trugs_agent").joinpath("payload")
        for name in FILES:
            if inspect(root, name) != before[name]:
                raise ValueError(f"destination changed: {name}")
        for name in FILES:
            data = payload.joinpath(name).read_bytes()
            with parent_fd(root, name, create=True) as (fd, leaf):
                flags = os.O_WRONLY | os.O_NOFOLLOW | os.O_NONBLOCK
                flags |= os.O_EXCL | os.O_CREAT if before[name] is None else 0
                child = os.open(leaf, flags, 0o644, dir_fd=fd)
                try:
                    info = os.fstat(child)
                    if not stat.S_ISREG(info.st_mode):
                        raise ValueError(f"not a regular file: {name}")
                    if before[name] is not None:
                        current = (
                            info.st_dev,
                            info.st_ino,
                            info.st_mtime_ns,
                            info.st_size,
                        )
                        if current != before[name]:
                            raise ValueError(f"destination changed: {name}")
                        if info.st_nlink != 1:
                            raise ValueError(f"hard-linked destination: {name}")
                    os.ftruncate(child, 0)
                    with os.fdopen(child, "wb", closefd=False) as stream:
                        stream.write(data)
                finally:
                    os.close(child)
    check(project)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version="trugs-agent 2.0.0")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("install", "check"):
        sub = commands.add_parser(name)
        sub.add_argument(
            "--project",
            default=".",
            help="existing project directory (default: current directory)",
        )
    args = parser.parse_args(argv)
    try:
        if args.command == "install":
            install(args.project)
        else:
            check(args.project)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
