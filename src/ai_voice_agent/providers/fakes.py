"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Deterministic, offline provider implementations.

These let the entire STT -> LLM -> TTS pipeline run and be tested without any
network access or API keys. They are intentionally simple but *self-consistent*:
:class:`FakeTTS` and :class:`FakeSTT` form a lossless round-trip, so a transcript
encoded to audio and decoded again recovers the original text exactly.
"""

from __future__ import annotations

from ai_voice_agent.providers.base import (
    LLM,
    STT,
    TTS,
    AudioChunk,
    LLMResponse,
    Message,
    Transcript,
)

_FAKE_MIME = "audio/l16"


class FakeTTS(TTS):
    """Encode text as UTF-8 bytes wrapped in an :class:`AudioChunk`.

    The encoding is reversible by :class:`FakeSTT`, which is what makes the
    fakes useful for end-to-end testing.
    """

    def __init__(self, sample_rate: int = 16_000) -> None:
        self.sample_rate = sample_rate

    def synthesize(self, text: str) -> AudioChunk:
        return AudioChunk(
            data=text.encode("utf-8"),
            mime_type=_FAKE_MIME,
            sample_rate=self.sample_rate,
        )


class FakeSTT(STT):
    """Decode audio produced by :class:`FakeTTS` back into text.

    ``confidence`` scales with payload size so empty audio is reported as a
    low-confidence, non-final transcript instead of a confident empty string.
    """

    def transcribe(self, audio: AudioChunk) -> Transcript:
        text = audio.data.decode("utf-8", errors="replace")
        if not text.strip():
            return Transcript(text="", confidence=0.0, is_final=False)
        return Transcript(text=text, confidence=1.0, is_final=True)


class FakeLLM(LLM):
    """A tiny rule-based dialog model.

    It is deterministic (same input -> same output) so tests never flake, yet
    it produces varied, context-aware replies that exercise the dialog manager:

    * greets back when greeted,
    * answers its own name when asked,
    * echoes the latest user message otherwise.
    """

    def __init__(self, name: str = "Vira") -> None:
        self.name = name

    def complete(self, messages: list[Message]) -> LLMResponse:
        user_turns = [m for m in messages if m.role == "user"]
        if not user_turns:
            return LLMResponse(text=f"Hello, this is {self.name}. How can I help you?")

        last = user_turns[-1].content.strip()
        lowered = last.lower()

        if any(word in lowered for word in ("hello", "hi", "hey")):
            text = f"Hi there! This is {self.name}. What can I do for you today?"
        elif "your name" in lowered or "who are you" in lowered:
            text = f"I'm {self.name}, an AI voice agent by Viprasol Tech."
        elif any(word in lowered for word in ("bye", "goodbye", "thank")):
            text = "Thanks for calling. Have a great day!"
        else:
            text = f"You said: {last}. How else can I help?"

        return LLMResponse(text=text, metadata={"model": "fake-llm", "turns": str(len(user_turns))})
