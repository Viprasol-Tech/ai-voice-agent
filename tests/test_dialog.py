"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Tests for the dialog manager: turn-taking and conversation state.
"""

from __future__ import annotations

import pytest

from ai_voice_agent.dialog import DialogManager, Speaker
from ai_voice_agent.providers.fakes import FakeLLM


def make_manager() -> DialogManager:
    return DialogManager(llm=FakeLLM(name="Vira"))


def test_starts_with_user_turn() -> None:
    dm = make_manager()
    assert dm.next_speaker is Speaker.USER
    assert dm.turn_count == 0


def test_turn_taking_alternates() -> None:
    dm = make_manager()
    dm.add_user_turn("hello")
    assert dm.next_speaker is Speaker.AGENT
    dm.respond()
    assert dm.next_speaker is Speaker.USER
    assert dm.turn_count == 2


def test_cannot_respond_out_of_turn() -> None:
    dm = make_manager()
    with pytest.raises(RuntimeError):
        dm.respond()


def test_cannot_add_two_user_turns_in_a_row() -> None:
    dm = make_manager()
    dm.add_user_turn("hello")
    with pytest.raises(RuntimeError):
        dm.add_user_turn("again")


def test_history_records_speakers_and_text() -> None:
    dm = make_manager()
    dm.add_user_turn("what is your name?")
    agent_turn = dm.respond()
    assert dm.history[0].speaker is Speaker.USER
    assert dm.history[1].speaker is Speaker.AGENT
    assert agent_turn.text == dm.history[1].text
    assert "Vira" in agent_turn.text


def test_reset_clears_history() -> None:
    dm = make_manager()
    dm.add_user_turn("hi")
    dm.respond()
    dm.reset()
    assert dm.turn_count == 0
    assert dm.next_speaker is Speaker.USER


def test_max_turns_trims_context_but_keeps_system_prompt() -> None:
    dm = DialogManager(llm=FakeLLM(), max_turns=2)
    for i in range(3):
        dm.add_user_turn(f"message {i}")
        dm.respond()
    messages = dm._build_messages()
    assert messages[0].role == "system"
    # system prompt + at most max_turns history entries
    assert len(messages) <= dm.max_turns + 1
