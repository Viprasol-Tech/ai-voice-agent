# Contributing to AI Voice Agent

Thanks for your interest in improving **AI Voice Agent** by [Viprasol Tech](https://viprasol.com)! 🎉

## Getting started

```bash
git clone https://github.com/Viprasol-Tech/ai-voice-agent.git
cd ai-voice-agent
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev,twilio]"
```

## Before you open a pull request

Please make sure the full local check suite is green:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy src
python -m pytest
```

This is exactly what CI runs across Ubuntu, macOS, and Windows on Python 3.11–3.13.

## Guidelines

- Keep the core package dependency-free; put new backends behind optional extras with **lazy imports**.
- Every provider should ship a deterministic offline fake or test double.
- Add tests for new behavior — we aim to keep the offline suite fully self-contained.
- Use clear, conventional commit messages (e.g. `feat:`, `fix:`, `docs:`).
- Be kind. By participating you agree to our [Code of Conduct](CODE_OF_CONDUCT.md).

## Reporting bugs & requesting features

Use the [issue templates](.github/ISSUE_TEMPLATE). For security issues, see [SECURITY.md](SECURITY.md).

Questions? Reach us at [support@viprasol.com](mailto:support@viprasol.com).
