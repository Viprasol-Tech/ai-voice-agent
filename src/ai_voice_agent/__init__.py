"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

AI Voice Agent — a small, dependency-light toolkit for building voice agents.

The pipeline is: speech-to-text (STT) -> LLM dialog manager -> text-to-speech (TTS).
Every provider is defined as an abstract base class with a deterministic, offline
"fake" implementation, so the whole stack runs and tests without network access or
API keys. Optional adapters (ElevenLabs TTS, Twilio webhook) are lazily imported.
"""

from __future__ import annotations

from ai_voice_agent.agent import VoiceAgent, VoiceReply
from ai_voice_agent.dialog import DialogManager, Turn
from ai_voice_agent.providers.base import (
    LLM,
    STT,
    TTS,
    AudioChunk,
    LLMResponse,
    Transcript,
)
from ai_voice_agent.providers.fakes import FakeLLM, FakeSTT, FakeTTS

__version__ = "0.1.0"

__all__ = [
    "LLM",
    "STT",
    "TTS",
    "AudioChunk",
    "DialogManager",
    "FakeLLM",
    "FakeSTT",
    "FakeTTS",
    "LLMResponse",
    "Transcript",
    "Turn",
    "VoiceAgent",
    "VoiceReply",
    "__version__",
]
