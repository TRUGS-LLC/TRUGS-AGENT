#!/usr/bin/env python3
"""Install this checkout into the current Python environment, offline."""

import shutil
import sys
import tempfile
import tomllib
from importlib.metadata import version
from pathlib import Path

from kit_check import ROOT, run
from packaging.requirements import Requirement


def main():
    requirements = tomllib.loads((ROOT / "installer/pyproject.toml").read_text())[
        "project"
    ]["dependencies"]
    for requirement in requirements:
        dependency = Requirement(requirement)
        if version(dependency.name) not in dependency.specifier:
            raise ValueError(
                "install the required runtime dependencies from your offline wheel bundle first"
            )
    with tempfile.TemporaryDirectory(prefix="kit-install-") as directory:
        temp = Path(directory)
        source = temp / "installer"
        shutil.copytree(ROOT / "installer", source)
        run(
            [
                sys.executable,
                "-m",
                "build",
                "--no-isolation",
                "--wheel",
                "--outdir",
                str(temp / "wheels"),
                str(source),
            ]
        )
        (wheel,) = (temp / "wheels").glob("*.whl")
        run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-index",
                "--find-links",
                str(temp / "wheels"),
                "--no-build-isolation",
                "--no-deps",
                "--force-reinstall",
                str(wheel),
            ]
        )
    print("PASS: local trugs-agent 2.0.0 installed")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
