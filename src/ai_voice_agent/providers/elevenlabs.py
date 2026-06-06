"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Optional ElevenLabs text-to-speech adapter.

The ``elevenlabs`` package and network access are only required at call time —
the import is performed lazily inside :meth:`ElevenLabsTTS.synthesize` so the
rest of the toolkit keeps working with zero extra dependencies.

Install the extra with::

    pip install "ai-voice-agent[elevenlabs]"
"""

from __future__ import annotations

import os

from ai_voice_agent.providers.base import TTS, AudioChunk


class ElevenLabsTTS(TTS):
    """Text-to-speech backed by the ElevenLabs API.

    Parameters
    ----------
    api_key:
        ElevenLabs API key. Falls back to the ``ELEVENLABS_API_KEY``
        environment variable when omitted.
    voice_id:
        The ElevenLabs voice to speak with.
    model_id:
        The ElevenLabs TTS model to use.
    """

    def __init__(
        self,
        api_key: str | None = None,
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",
        model_id: str = "eleven_multilingual_v2",
    ) -> None:
        self.api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
        if not self.api_key:
            msg = (
                "An ElevenLabs API key is required. Pass api_key=... or set the "
                "ELEVENLABS_API_KEY environment variable."
            )
            raise ValueError(msg)
        self.voice_id = voice_id
        self.model_id = model_id

    def synthesize(self, text: str) -> AudioChunk:
        try:
            from elevenlabs.client import ElevenLabs  # noqa: PLC0415
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            msg = (
                "The 'elevenlabs' package is not installed. Install it with "
                "pip install 'ai-voice-agent[elevenlabs]'."
            )
            raise ImportError(msg) from exc

        client = ElevenLabs(api_key=self.api_key)
        stream = client.text_to_speech.convert(
            voice_id=self.voice_id,
            model_id=self.model_id,
            text=text,
            output_format="mp3_44100_128",
        )
        audio = b"".join(stream)
        return AudioChunk(data=audio, mime_type="audio/mpeg", sample_rate=44_100)
