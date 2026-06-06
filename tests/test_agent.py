"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Tests for the end-to-end VoiceAgent pipeline.
"""

from __future__ import annotations

from ai_voice_agent.agent import VoiceAgent, VoiceReply
from ai_voice_agent.providers.fakes import FakeLLM, FakeSTT, FakeTTS


def make_agent() -> VoiceAgent:
    return VoiceAgent(stt=FakeSTT(), llm=FakeLLM(name="Vira"), tts=FakeTTS())


def test_handle_text_full_turn() -> None:
    agent = make_agent()
    reply = agent.handle_text("Hello there")
    assert isinstance(reply, VoiceReply)
    assert reply.transcript.text == "Hello there"
    assert "Vira" in reply.reply_text
    assert len(reply.audio) > 0


def test_handle_audio_uses_stt() -> None:
    agent = make_agent()
    inbound = FakeTTS().synthesize("what is your name?")
    reply = agent.handle_audio(inbound)
    assert reply.transcript.text == "what is your name?"
    assert "Vira" in reply.reply_text


def test_pipeline_audio_is_replayable() -> None:
    agent = make_agent()
    reply = agent.handle_text("hello")
    # The reply audio can be decoded back to the reply text by FakeSTT.
    decoded = FakeSTT().transcribe(reply.audio)
    assert decoded.text == reply.reply_text


def test_multi_turn_conversation_keeps_state() -> None:
    agent = make_agent()
    agent.handle_text("hello")
    agent.handle_text("what is your name?")
    assert agent.dialog.turn_count == 4
