# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-06-06

### Added

- Initial release of the **AI Voice Agent** toolkit by Viprasol Tech.
- Pluggable `STT` / `TTS` / `LLM` abstract base classes with deterministic offline fakes.
- `VoiceAgent` end-to-end pipeline wiring speech-to-text → LLM dialog → text-to-speech.
- `DialogManager` with turn-taking and conversation state.
- Optional ElevenLabs TTS adapter (lazy import, `elevenlabs` extra).
- Optional Twilio telephony webhook returning TwiML via FastAPI (`twilio` extra).
- CLI for a text-simulated conversation (`python -m ai_voice_agent`).
- Typed end to end (`py.typed`, `mypy --strict`).
- Tooling: ruff, mypy strict, pytest, multi-OS CI, Docker.

[Unreleased]: https://github.com/Viprasol-Tech/ai-voice-agent/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Viprasol-Tech/ai-voice-agent/releases/tag/v0.1.0
