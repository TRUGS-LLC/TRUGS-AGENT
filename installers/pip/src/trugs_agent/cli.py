"""Initialize TRUGS Agent in the current project directory."""

import argparse
import shutil
import sys
from pathlib import Path

TEMPLATES = Path(__file__).parent / "templates"

IDE_FILES = {
    "claude": "CLAUDE.md",
    "cursor": ".cursorrules",
    "copilot": ".github/copilot-instructions.md",
}

COMPONENTS = ["AAA", "EPIC", "FOLDER", "MEMORY", "SKILLS", "TRUGGING", "WEB_HUB"]


def main():
    parser = argparse.ArgumentParser(
        description="Initialize TRUGS Agent in your project"
    )
    parser.add_argument(
        "ide",
        nargs="?",
        default="claude",
        choices=["claude", "cursor", "copilot"],
        help="Target IDE (default: claude)",
    )
    args = parser.parse_args()

    dest = Path.cwd()
    target_file = IDE_FILES[args.ide]
    target_path = dest / target_file

    # Copy AGENT.md as IDE-specific file
    agent_src = TEMPLATES / "AGENT.md"
    if not agent_src.exists():
        print(f"Error: templates not found at {TEMPLATES}", file=sys.stderr)
        sys.exit(1)

    if target_path.exists():
        print(f"{target_file} already exists — skipping (won't overwrite)")
    else:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(agent_src, target_path)
        print(f"Created {target_file}")

    # Copy component folders
    copied = 0
    for comp in COMPONENTS:
        src_dir = TEMPLATES / comp
        dest_dir = dest / comp
        if not src_dir.exists():
            continue
        if dest_dir.exists():
            print(f"{comp}/ already exists — skipping")
            continue
        shutil.copytree(src_dir, dest_dir)
        copied += 1
        print(f"Created {comp}/")

    # Copy validator
    tools_src = TEMPLATES / "tools"
    tools_dest = dest / "tools"
    if tools_src.exists() and not tools_dest.exists():
        shutil.copytree(tools_src, tools_dest)
        print("Created tools/ (validator)")

    print(f"\nTRUGS Agent initialized for {args.ide}. Your LLM now speaks TRUG/L.")
    print(f"  {target_file} — TRUG/L vocabulary and grammar")
    if copied > 0:
        print(f"  {copied} component folders — methodology and tools")
    print("\nFull docs: https://github.com/TRUGS-LLC/TRUGS-AGENT")
