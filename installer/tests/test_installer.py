"""Installer boundaries and installed-file language checks."""

import io
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "installer/src"))
from trugs_agent import cli  # noqa: E402


class Terminal(io.StringIO):
    def isatty(self):
        return True


def test_install_lists_before_write_and_checks(tmp_path, capsys):
    project = tmp_path / "project"
    project.mkdir()
    cli.install(project)
    output = capsys.readouterr().out
    assert output.startswith(
        "Files to place:\n" + "".join(f"  {name}\n" for name in cli.FILES)
    )
    assert output.endswith("PASS: trugs-agent check\n")
    assert sorted(
        p.relative_to(project).as_posix() for p in project.rglob("*") if p.is_file()
    ) == sorted(cli.FILES)
    cli.check(project)


@pytest.mark.parametrize(
    "answer,terminal", [("no\n", True), ("\n", True), ("yes\n", False)]
)
def test_no_or_nonterminal_preserves_everything(
    tmp_path, monkeypatch, answer, terminal
):
    (tmp_path / "AGENTS.md").write_text("mine\n")
    monkeypatch.setattr(
        sys, "stdin", Terminal(answer) if terminal else io.StringIO(answer)
    )
    with pytest.raises(ValueError):
        cli.install(tmp_path)
    assert (tmp_path / "AGENTS.md").read_text() == "mine\n"
    assert [p.name for p in tmp_path.iterdir()] == ["AGENTS.md"]


def test_terminal_yes_replaces_and_checks(tmp_path, monkeypatch):
    (tmp_path / "AGENTS.md").write_text("old\n")
    monkeypatch.setattr(sys, "stdin", Terminal("yes\n"))
    cli.install(tmp_path)
    assert "TRUGS agent entry" in (tmp_path / "AGENTS.md").read_text()


@pytest.mark.parametrize("mode", ["project", "parent", "file", "hardlink"])
def test_outside_files_unchanged(tmp_path, mode, monkeypatch):
    project, outside = tmp_path / "project", tmp_path / "outside"
    project.mkdir()
    outside.mkdir()
    sentinel = outside / "keep"
    sentinel.write_text("outside\n")
    if mode == "project":
        project.rmdir()
        project.symlink_to(outside, target_is_directory=True)
    elif mode == "parent":
        (project / ".cursor").symlink_to(outside, target_is_directory=True)
    elif mode == "file":
        (project / "AGENTS.md").symlink_to(sentinel)
    else:
        os.link(sentinel, project / "AGENTS.md")
    monkeypatch.setattr(sys, "stdin", Terminal("yes\n"))
    with pytest.raises((ValueError, OSError)):
        cli.install(project)
    assert sentinel.read_text() == "outside\n"
    assert [p.name for p in outside.iterdir()] == ["keep"]


@pytest.mark.parametrize("kind", ["syntax", "vocabulary", "fence", "missing", "plugin"])
def test_check_rejects_broken_placed_file(tmp_path, kind):
    cli.install(tmp_path)
    target = tmp_path / "AGENTS.md"
    if kind == "syntax":
        target.write_text("```trl\nPIPELINE bad SHALL VALIDATE.\n```\n")
    elif kind == "vocabulary":
        target.write_text("```trl\nPARTY bad FROBNICATE.\n```\n")
    elif kind == "fence":
        target.write_text("```trl\nPARTY bad VALIDATE.\n")
    elif kind == "missing":
        target.unlink()
    else:
        (tmp_path / ".claude-plugin/plugin.json").write_text("{}")
    with pytest.raises((ValueError, OSError, KeyError)):
        cli.check(tmp_path)


def test_check_rejects_linked_placed_file(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    cli.install(project)
    outside = tmp_path / "outside"
    outside.write_text((project / "AGENTS.md").read_text())
    (project / "AGENTS.md").unlink()
    (project / "AGENTS.md").symlink_to(outside)
    with pytest.raises(OSError):
        cli.check(project)
