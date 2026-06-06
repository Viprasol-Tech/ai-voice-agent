"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Provider interfaces (STT / TTS / LLM) and their offline fake implementations.
"""

from __future__ import annotations

from ai_voice_agent.providers.base import (
    LLM,
    STT,
    TTS,
    AudioChunk,
    LLMResponse,
    Transcript,
)
from ai_voice_agent.providers.fakes import FakeLLM, FakeSTT, FakeTTS

__all__ = [
    "LLM",
    "STT",
    "TTS",
    "AudioChunk",
    "FakeLLM",
    "FakeSTT",
    "FakeTTS",
    "LLMResponse",
    "Transcript",
]
