#!/usr/bin/env bash
# Sync template files from repo root into npm and pip installer packages.
# Run this from the repo root before publishing either package.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPONENTS="AAA EPIC FOLDER MEMORY SKILLS TRUGGING WEB_HUB"

for target in npm/templates pip/src/trugs_agent/templates; do
    dest="$REPO_ROOT/installers/$target"
    rm -rf "$dest"
    mkdir -p "$dest"

    # Copy root AGENT.md
    cp "$REPO_ROOT/AGENT.md" "$dest/AGENT.md"

    # Copy component folders (AGENT.md + README.md + examples)
    for comp in $COMPONENTS; do
        if [ -d "$REPO_ROOT/$comp" ]; then
            cp -r "$REPO_ROOT/$comp" "$dest/$comp"
        fi
    done

    # Copy validator tools
    if [ -d "$REPO_ROOT/tools" ]; then
        cp -r "$REPO_ROOT/tools" "$dest/tools"
    fi

    echo "Synced templates to installers/$target"
done
