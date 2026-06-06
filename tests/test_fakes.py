"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Tests for the offline fake providers and their round-trip guarantee.
"""

from __future__ import annotations

from ai_voice_agent.providers.base import AudioChunk, Message
from ai_voice_agent.providers.fakes import FakeLLM, FakeSTT, FakeTTS


def test_tts_returns_audio_chunk() -> None:
    chunk = FakeTTS().synthesize("hello world")
    assert isinstance(chunk, AudioChunk)
    assert len(chunk) > 0
    assert chunk.mime_type == "audio/l16"


def test_stt_tts_roundtrip_is_lossless() -> None:
    text = "The quick brown fox jumps over the lazy dog."
    audio = FakeTTS().synthesize(text)
    transcript = FakeSTT().transcribe(audio)
    assert transcript.text == text
    assert transcript.is_final is True
    assert transcript.confidence == 1.0


def test_stt_on_empty_audio_is_low_confidence() -> None:
    transcript = FakeSTT().transcribe(AudioChunk(data=b""))
    assert transcript.text == ""
    assert transcript.confidence == 0.0
    assert transcript.is_final is False


def test_llm_greets_back() -> None:
    response = FakeLLM(name="Vira").complete([Message(role="user", content="Hello!")])
    assert "Vira" in response.text


def test_llm_answers_name_question() -> None:
    response = FakeLLM(name="Vira").complete([Message(role="user", content="what is your name?")])
    assert "Vira" in response.text


def test_llm_is_deterministic() -> None:
    msgs = [Message(role="user", content="schedule a demo")]
    first = FakeLLM().complete(msgs)
    second = FakeLLM().complete(msgs)
    assert first.text == second.text


def test_llm_handles_empty_conversation() -> None:
    response = FakeLLM(name="Vira").complete([])
    assert "Vira" in response.text
