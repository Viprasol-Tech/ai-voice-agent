"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Optional Twilio telephony webhook built on FastAPI.

FastAPI is imported lazily inside :func:`create_twilio_app` so the dependency is
only needed when you actually serve telephony. Twilio posts speech-recognition
results to the webhook; we run them through a :class:`VoiceAgent` and answer with
TwiML that speaks the reply and gathers the caller's next utterance.

Install the extra with::

    pip install "ai-voice-agent[twilio]"
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from xml.sax.saxutils import escape

from ai_voice_agent.agent import VoiceAgent

if TYPE_CHECKING:  # pragma: no cover - typing only
    from fastapi import FastAPI


def build_twiml(say_text: str, action_path: str = "/twilio/voice") -> str:
    """Render a TwiML document that speaks ``say_text`` then gathers speech.

    The text is XML-escaped so arbitrary LLM output cannot break the document.
    """
    safe = escape(say_text)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response>"
        f'<Gather input="speech" action="{escape(action_path)}" method="POST" '
        'speechTimeout="auto">'
        f"<Say>{safe}</Say>"
        "</Gather>"
        f'<Redirect method="POST">{escape(action_path)}</Redirect>'
        "</Response>"
    )


def create_twilio_app(agent: VoiceAgent, action_path: str = "/twilio/voice") -> FastAPI:
    """Create a FastAPI app exposing a single Twilio voice webhook.

    Parameters
    ----------
    agent:
        The :class:`VoiceAgent` that powers each turn.
    action_path:
        The route Twilio posts to (and that ``<Gather>`` loops back to).
    """
    try:
        from fastapi import FastAPI, Form, Request, Response  # noqa: PLC0415
    except ImportError as exc:  # pragma: no cover - exercised only without the extra
        msg = "FastAPI is not installed. Install it with pip install 'ai-voice-agent[twilio]'."
        raise ImportError(msg) from exc

    app = FastAPI(title="AI Voice Agent — Twilio Webhook")

    @app.post(action_path)
    async def voice(
        request: Request,
        SpeechResult: str = Form(default=""),  # noqa: N803 - Twilio field name
    ) -> Any:
        caller_text = SpeechResult.strip()
        if not caller_text:
            twiml = build_twiml(
                "Hello, you've reached the Viprasol AI voice agent. How can I help?",
                action_path=action_path,
            )
        else:
            reply = agent.handle_text(caller_text)
            twiml = build_twiml(reply.reply_text, action_path=action_path)
        return Response(content=twiml, media_type="application/xml")

    return app
