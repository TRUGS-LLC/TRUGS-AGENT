# Contributing to TRUGS Agent

Thanks for your interest in contributing. Every contribution matters — from fixing a typo to adding a new component.

## Quick Links

- [Issues](https://github.com/TRUGS-LLC/TRUGS-AGENT/issues) — bug reports, feature requests, and tasks
- [Discussions](https://github.com/TRUGS-LLC/TRUGS-AGENT/discussions) — questions, ideas, and general conversation
- [TRL Specification](https://github.com/TRUGS-LLC/TRUGS) — the full TRUGS and TRL spec

## How to Contribute

### Report a Bug or Request a Feature

Open an [issue](https://github.com/TRUGS-LLC/TRUGS-AGENT/issues/new). Include:
- What you expected to happen
- What actually happened
- Steps to reproduce (if applicable)

### Fix a Bug or Add a Feature

1. Fork the repo
2. Create a branch: `git checkout -b fix/description` or `feat/description`
3. Make your changes
4. Validate any TRUGs you touched: `python tools/kit_check.py --repositories PATH_TO_SOURCES`
5. Submit a pull request

### Improve Documentation

Documentation improvements are always welcome. This includes:
- Fixing typos or unclear wording
- Adding examples to component READMEs
- Improving AGENTS.md instructions
- Adding use cases or tutorials

### Add a New Example

Have you used TRUGS Agent in a real project? We'd love to include it in `examples/`. See [examples/README.md](examples/README.md) for the format.

## Good First Issues

Look for issues labeled [`good first issue`](https://github.com/TRUGS-LLC/TRUGS-AGENT/labels/good%20first%20issue). These are scoped, well-defined tasks that don't require deep knowledge of the system.

## Writing TRL

When contributing TRL content (AGENTS.md files, examples, specifications), use words from the [installed vocabulary](PRIMER.md#vocabulary). Do not invent new words — every TRL word has exactly one meaning.

Quick reference:
- **SHALL** = must do (obligation)
- **MAY** = allowed (permission)
- **SHALL_NOT** = must not do (prohibition)
- Sugar words (`'of`, `'is`, `'with`) are for readability — they compile to nothing

## Code Style

- Python code follows standard Python conventions (PEP 8)
- The kit consumes the published language tools rather than copying the validator
- Tests use pytest

## Branch Naming

- `fix/description` — bug fixes
- `feat/description` — new features
- `docs/description` — documentation changes

## Pull Request Process

1. Describe what your PR does and why
2. Reference any related issues
3. Make sure tests pass
4. A maintainer will review and merge

## License

By contributing, you agree that your contributions will be licensed under the [Apache 2.0 License](LICENSE).

Use `python tools/kit_check.py --repositories PATH_TO_SOURCES --generate` after editing instruction sources or
lessons, then `python tools/kit_check.py --repositories PATH_TO_SOURCES` and the installer tests. Folder indices
come from trugs-web map. Generation never edits a hand-maintained graph.

The workflow runs on every push and pull request. It installs trugs-tools 2.4.0
and trugs-web 2.1.0 from the Python package index and checks out the public
repositories at the revisions in map/repositories.json. It prepares a wheelhouse
from the index before running the checks offline. No private checkout is needed.

The manual workflow consumes a prepared kit-inputs artifact from a named run.
Its wheelhouse must include trugs-web 2.1.0, the runtime dependencies and all
build/test wheels; its repositories directory must retain the public checkouts'
git metadata at the revisions in map/repositories.json. Rust and cargo must be
available on the runner. Both workflow jobs check a temporary copy, so building
or installing the package leaves the source checkout clean.

Run the checker on a temporary copy of the tree, with `--repositories` pointing
to those checkouts and `--wheelhouse` pointing to the prepared wheelhouse. The
checker defaults to a wheelhouse beside the active virtual environment if that
option is omitted. It builds trugs-agent 2.0.0 from a scratch copy under its
temporary directory, then executes each documented command verbatim in a fresh
virtual environment. For stated index installs, pip is configured with no index,
only the prepared wheelhouse and that freshly built wheel, and no build isolation.
Any trugs-agent wheel in the input bundle is excluded in favour of the fresh build.
Their stdout and exit status are compared with the expectations beside the commands.
Pass the same `--wheelhouse` to the installer tests. No network is used during
kit_check or the installer tests.

To install from a checkout with build tools and runtime dependencies already
available, the helper builds in temporary storage and installs the wheel into the
current Python environment; it does not place instructions in the checkout:

```sh
python tools/install_local.py
```
<!-- expect: {"status": 0, "stdout": "PASS: local trugs-agent 2.0.0 installed\n"} -->

Expected stdout: `PASS: local trugs-agent 2.0.0 installed`; exit status 0.

The index includes hidden directories. Its input is a copy of the tree
without folder.trug.json; the output is written outside that copy.
