"""Container fences and every printed command's promised result."""

import json
import shutil
import subprocess
import sys
import sysconfig
import venv
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from kit_check import blocks  # noqa: E402
from kit_parts import command_environment, commands  # noqa: E402

CONTAINERS = (
    "{fence}trl\t\n{body}\n{fence}\n",
    "> {fence}trl\n> {body}\n> {fence}\n",
    "> > {fence}trl\n> > {body}\n> > {fence}\n",
    "- Lesson\n\n  {fence}trl\n  {body}\n  {fence}\n",
    "10. Lesson\n\n    {fence}trl\n    {body}\n    {fence}\n",
    "> - {fence}trl\n>   {body}\n>   {fence}\n",
    "- > {fence}trl\n  > {body}\n  > {fence}\n",
)


@pytest.mark.parametrize("container", CONTAINERS)
@pytest.mark.parametrize("fence", ("```", "~~~"))
def test_fence_bodies_follow_container_rules(container, fence):
    body = "PARTY lesson VALIDATE."
    text = container.format(fence=fence, body=body)
    assert list(blocks(text)) == [("trl", body + "\n")]
    # Fence-looking text inside an ordinary code block is not TRL.
    assert list(blocks("````text\n" + text + "````\n")) == [("text", text)]


@pytest.mark.parametrize("container", CONTAINERS)
@pytest.mark.parametrize("fence", ("```", "~~~"))
def test_full_kit_entry_rejects_container_trl(tmp_path, container, fence):
    tree = tmp_path / "kit"
    shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns(".git"))
    document = tree / "examples/hello/README.md"
    document.write_text(
        document.read_text()
        + "\n"
        + container.format(fence=fence, body="PARTY broken FROBNICATE.")
    )
    result = subprocess.run(
        [
            sys.executable,
            str(tree / "tools/kit_check.py"),
            "--generate",
            "--repositories",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "FROBNICATE" in result.stderr
    assert "PASS: kit_check" not in result.stdout


@pytest.fixture(scope="module")
def installed_wheel(tmp_path_factory):
    temp = tmp_path_factory.mktemp("wheel-fences")
    source = temp / "installer"
    shutil.copytree(ROOT / "installer", source)
    wheels = temp / "wheels"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "build",
            "--no-isolation",
            "--wheel",
            "--outdir",
            str(wheels),
            str(source),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    environment = temp / "venv"
    venv.EnvBuilder(with_pip=True, system_site_packages=True).create(environment)
    python = environment / "bin/python"
    purelib = Path(
        subprocess.run(
            [
                str(python),
                "-c",
                "import sysconfig; print(sysconfig.get_path('purelib'))",
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    )
    (purelib / "prepared-runtime.pth").write_text(sysconfig.get_path("purelib") + "\n")
    subprocess.run(
        [
            str(environment / "bin/python"),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--no-build-isolation",
            "--no-deps",
            "--ignore-installed",
            str(next(wheels.glob("*.whl"))),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return environment / "bin/trugs-agent"


@pytest.mark.parametrize("container", CONTAINERS)
@pytest.mark.parametrize("fence", ("```", "~~~"))
def test_installed_wheel_checks_container_trl(
    tmp_path, installed_wheel, container, fence
):
    subprocess.run(
        [str(installed_wheel), "install", "--project", str(tmp_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    document = tmp_path / "AGENTS.md"
    original = document.read_text()
    document.write_text(
        original
        + "\n"
        + container.format(fence=fence, body="PARTY lesson VALIDATE.")
        + "\n```text\nPARTY ignored FROBNICATE.\n```\n"
    )
    result = subprocess.run(
        [str(installed_wheel), "check", "--project", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    document.write_text(
        original + "\n" + container.format(fence=fence, body="PARTY broken FROBNICATE.")
    )
    result = subprocess.run(
        [str(installed_wheel), "check", "--project", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "FROBNICATE" in result.stderr


def command_fixture(tmp_path, monkeypatch, second):
    (tmp_path / "kit/skills").mkdir(parents=True)
    script = tmp_path / "examples/calculator/check.sh"
    script.parent.mkdir(parents=True)
    script.write_text(
        "printf x >> executions\n"
        'test "$1" = --repositories && test "$2" = "$repositories" || exit 8\n'
        'test "$3" = --calculator-source && test "$4" = "$calculator_source" || exit 9\n'
        'test "$5" = printed-argument || exit 10\n'
        'printf "PASS: command\\n"\n'
    )
    command = (
        'bash examples/calculator/check.sh --repositories "$repositories" '
        '--calculator-source "$calculator_source" printed-argument'
    )
    expected = {"status": 0, "stdout": "PASS: command\n"}
    for name, result in (("README.md", expected), ("PRIMER.md", second)):
        (tmp_path / name).write_text(
            "# Lesson\n\n```sh\n"
            + command
            + "\n```\n<!-- expect: "
            + json.dumps(result)
            + " -->\n"
        )
    # Installer behavior has separate CLI/wheel tests; run these shell lessons directly.
    monkeypatch.setattr("kit_parts.run", lambda *args, **kwargs: "")
    return tmp_path / "repositories with spaces", tmp_path / "calculator with spaces"


def test_command_is_verbatim_and_each_occurrence_matches(tmp_path, monkeypatch, capsys):
    inputs = command_fixture(
        tmp_path, monkeypatch, {"status": 0, "stdout": "PASS: command\n"}
    )
    commands(tmp_path, tmp_path, *inputs)
    assert (tmp_path / "executions").read_text() == "x"
    assert "2 stated commands, 1 distinct" in capsys.readouterr().out


@pytest.mark.parametrize(
    "second",
    (
        {"status": 0, "stdout": "IMPOSSIBLE\n"},
        {"status": 7, "stdout": "PASS: command\n"},
    ),
)
def test_every_occurrence_checks_stdout_and_status(tmp_path, monkeypatch, second):
    inputs = command_fixture(tmp_path, monkeypatch, second)
    with pytest.raises(ValueError) as failure:
        commands(tmp_path, tmp_path, *inputs)
    message = str(failure.value)
    assert "PRIMER.md:4" in message
    assert "README.md:4" in message
    assert "contradictory expectations" in message
    assert (tmp_path / "executions").read_text() == "x"


def shell_block(container, fence, kind, command, expected):
    prefix = container.rsplit("{fence}", 1)[0].rsplit("\n", 1)[-1]
    return container.replace("trl", kind).format(fence=fence, body=command) + (
        prefix + "<!-- expect: " + json.dumps(expected) + " -->\n"
    )


@pytest.mark.parametrize("container", CONTAINERS)
@pytest.mark.parametrize("fence", ("```", "~~~"))
@pytest.mark.parametrize("kind", ("sh", "bash", "shell"))
def test_command_containers_execute_and_compare(
    tmp_path, monkeypatch, capsys, container, fence, kind
):
    expected = {"status": 0, "stdout": "PASS: command\n"}
    inputs = command_fixture(tmp_path, monkeypatch, expected)
    document = tmp_path / "PRIMER.md"
    command = next(iter(blocks(document.read_text())))[1].rstrip("\n")
    document.write_text(shell_block(container, fence, kind, command, expected))
    commands(tmp_path, tmp_path, *inputs)
    assert (tmp_path / "executions").read_text() == "x"
    assert "2 stated commands, 1 distinct" in capsys.readouterr().out


@pytest.mark.parametrize(
    "name",
    (
        "CONTRIBUTING.md",
        "map/README.md",
        "kit/primer.md.in",
        "installer/src/trugs_agent/payload/extra.md",
    ),
)
def test_commands_in_every_markdown_document(tmp_path, monkeypatch, name):
    inputs = command_fixture(
        tmp_path, monkeypatch, {"status": 0, "stdout": "PASS: command\n"}
    )
    document = tmp_path / name
    document.parent.mkdir(parents=True, exist_ok=True)
    document.write_text(
        shell_block(
            CONTAINERS[1],
            "~~~",
            "sh",
            "printf actual",
            {"status": 0, "stdout": "false"},
        )
    )
    with pytest.raises(ValueError, match="command differs at " + name + ":2"):
        commands(tmp_path, tmp_path, *inputs)


@pytest.mark.parametrize(
    "tail",
    (
        "",
        "> <!-- expect: invalid -->\n",
        '> <!-- expect: {"status": 0} -->\n',
        '<!-- expect: {"status": 0, "stdout": "actual"} -->\n',
    ),
)
def test_missing_or_invalid_container_expectation_fails(tmp_path, monkeypatch, tail):
    inputs = command_fixture(
        tmp_path, monkeypatch, {"status": 0, "stdout": "PASS: command\n"}
    )
    (tmp_path / "PRIMER.md").write_text("> ~~~sh\n> printf actual\n> ~~~\n" + tail)
    with pytest.raises(ValueError, match="expected|expectation") as failure:
        commands(tmp_path, tmp_path, *inputs)
    assert "PRIMER.md:2" in str(failure.value)


@pytest.mark.parametrize("container", (CONTAINERS[1], CONTAINERS[3]))
@pytest.mark.parametrize("fence", ("```", "~~~"))
@pytest.mark.parametrize("fault", ("stdout", "status"))
def test_full_kit_entry_rejects_container_command_result(
    tmp_path, prepared_repositories, prepared_wheelhouse, container, fence, fault
):
    tree = tmp_path / "kit"
    shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns(".git"))
    document = tree / "kit/skills/compile-decompile/SKILL.md"
    text = document.read_text()
    if fault == "stdout":
        text = text.replace("PASS: hello", "IMPOSSIBLE")
    else:
        text = text.replace('"status": 0', '"status": 7').replace(
            "exit status 0", "exit status 7"
        )
    start = text.index("```sh\n")
    end = text.index("-->\n", start) + 4
    command = "bash examples/hello/check.sh"
    expected = {
        "status": 7 if fault == "status" else 0,
        "stdout": "IMPOSSIBLE\n" if fault == "stdout" else "PASS: hello\n",
    }
    text = (
        text[:start]
        + shell_block(container, fence, "sh", command, expected)
        + text[end:]
    )
    document.write_text(text)
    body_line = text[: text.index(command)].count("\n") + 1
    args = [
        sys.executable,
        str(tree / "tools/kit_check.py"),
        "--repositories",
        str(prepared_repositories),
        "--wheelhouse",
        str(prepared_wheelhouse),
    ]
    # Regenerate normally first, so stale-index rejection cannot mask the fault.
    for extra in (["--generate"], []):
        result = subprocess.run(
            args + extra, cwd=tree, capture_output=True, text=True, check=False
        )
        assert result.returncode == 1, result.stdout + result.stderr
        assert (
            f"command differs at kit/skills/compile-decompile/SKILL.md:{body_line}"
            in result.stderr
        )
        readme = (tree / "README.md").read_text()
        first_line = readme[: readme.index(command)].count("\n") + 1
        assert f"first stated at README.md:{first_line}" in result.stderr
        assert "PASS: kit_check" not in result.stdout


def test_printed_index_install_uses_local_wheels_only(tmp_path, prepared_wheelhouse):
    scratch = tmp_path / "scratch with spaces"
    scratch.mkdir()
    bundle = tmp_path / "input wheels"
    bundle.mkdir()
    for wheel in prepared_wheelhouse.glob("*.whl"):
        if not wheel.name.lower().startswith("trugs_agent-"):
            (bundle / wheel.name).symlink_to(wheel)
    # This same-version input must never replace the newly built kit wheel.
    (bundle / "trugs_agent-2.0.0-py3-none-any.whl").write_bytes(b"stale input")
    env = command_environment(ROOT, scratch, bundle)
    command = next(
        body for kind, body in blocks((ROOT / "README.md").read_text()) if kind == "sh"
    )
    result = subprocess.run(
        ["bash", "-c", command],
        env=env,
        cwd=scratch,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout == ""
    result = subprocess.run(
        [str(scratch / "command-venv/bin/trugs-agent"), "--version"],
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    assert result.stdout == "trugs-agent 2.0.0\n"
    result = subprocess.run(
        [
            str(scratch / "command-venv/bin/python"),
            "-m",
            "pip",
            "install",
            "trugs-agent==0.0.0",
        ],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    assert "No matching distribution found" in result.stderr
    assert "Retrying" not in result.stderr
