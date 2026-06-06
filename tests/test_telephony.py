"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Tests for the Twilio TwiML builder (pure, no FastAPI required).
"""

from __future__ import annotations

from ai_voice_agent.telephony import build_twiml


def test_twiml_is_well_formed() -> None:
    twiml = build_twiml("Hello caller")
    assert twiml.startswith("<?xml")
    assert "<Response>" in twiml
    assert "<Say>Hello caller</Say>" in twiml
    assert '<Gather input="speech"' in twiml


def test_twiml_escapes_user_content() -> None:
    twiml = build_twiml('5 < 6 & "quoted"')
    assert "&lt;" in twiml
    assert "&amp;" in twiml
    assert "< 6" not in twiml


def test_twiml_uses_custom_action_path() -> None:
    twiml = build_twiml("hi", action_path="/custom/hook")
    assert "/custom/hook" in twiml
