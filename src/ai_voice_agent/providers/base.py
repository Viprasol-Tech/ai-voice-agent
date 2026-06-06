"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Provider abstract base classes and the small data types passed between stages.

Three roles make up the pipeline:

* ``STT`` turns inbound audio into a :class:`Transcript`.
* ``LLM`` turns a list of chat messages into an :class:`LLMResponse`.
* ``TTS`` turns assistant text into an :class:`AudioChunk`.

Concrete providers (offline fakes, ElevenLabs, ...) subclass these.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Literal

Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True, slots=True)
class AudioChunk:
    """A self-describing block of raw audio bytes.

    The fakes use ``audio/l16`` PCM-like payloads, but the dataclass is
    format-agnostic so real adapters can return MP3, mu-law, etc.
    """

    data: bytes
    mime_type: str = "audio/l16"
    sample_rate: int = 16_000

    def __len__(self) -> int:
        return len(self.data)


@dataclass(frozen=True, slots=True)
class Transcript:
    """The text recovered from a chunk of audio, with a confidence score."""

    text: str
    confidence: float = 1.0
    is_final: bool = True


@dataclass(frozen=True, slots=True)
class Message:
    """A single chat message in an LLM conversation."""

    role: Role
    content: str


@dataclass(frozen=True, slots=True)
class LLMResponse:
    """The assistant text returned by an :class:`LLM`, plus metadata."""

    text: str
    finish_reason: str = "stop"
    metadata: dict[str, str] = field(default_factory=dict)


class STT(ABC):
    """Speech-to-text provider interface."""

    @abstractmethod
    def transcribe(self, audio: AudioChunk) -> Transcript:
        """Convert a chunk of audio into a :class:`Transcript`."""
        raise NotImplementedError


class TTS(ABC):
    """Text-to-speech provider interface."""

    @abstractmethod
    def synthesize(self, text: str) -> AudioChunk:
        """Convert text into an :class:`AudioChunk`."""
        raise NotImplementedError


class LLM(ABC):
    """Large-language-model provider interface."""

    @abstractmethod
    def complete(self, messages: list[Message]) -> LLMResponse:
        """Produce the assistant's reply given the conversation so far."""
        raise NotImplementedError
