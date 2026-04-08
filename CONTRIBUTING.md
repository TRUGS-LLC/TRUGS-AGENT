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
4. Run the validator tests: `python -m pytest tools/test_validate.py`
5. Submit a pull request

### Improve Documentation

Documentation improvements are always welcome. This includes:
- Fixing typos or unclear wording
- Adding examples to component READMEs
- Improving AGENT.md instructions
- Adding use cases or tutorials

### Add a New Example

Have you used TRUGS Agent in a real project? We'd love to include it in `examples/`. See [examples/README.md](examples/README.md) for the format.

## Good First Issues

Look for issues labeled [`good first issue`](https://github.com/TRUGS-LLC/TRUGS-AGENT/labels/good%20first%20issue). These are scoped, well-defined tasks that don't require deep knowledge of the system.

## Writing TRL

When contributing TRL content (AGENT.md files, examples, specifications), use words from the [190-word TRL vocabulary](AGENT.md#trl--the-language). Do not invent new words — every TRL word has exactly one meaning.

Quick reference:
- **SHALL** = must do (obligation)
- **MAY** = allowed (permission)
- **SHALL_NOT** = must not do (prohibition)
- Sugar words (`'of`, `'is`, `'with`) are for readability — they compile to nothing

## Code Style

- Python code follows standard Python conventions (PEP 8)
- No external dependencies in core tools — the validator is zero-dependency by design
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
