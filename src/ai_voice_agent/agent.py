"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

The :class:`VoiceAgent` pipeline wires the three stages together:

    inbound audio --STT--> text --LLM (via DialogManager)--> reply text --TTS--> audio

It is deliberately thin: all the conversational state lives in
:class:`~ai_voice_agent.dialog.DialogManager`, and all the I/O lives in the
provider implementations. That keeps the agent easy to test and to retarget at
real STT/TTS/LLM backends.
"""

from __future__ import annotations

from dataclasses import dataclass

from ai_voice_agent.dialog import DialogManager
from ai_voice_agent.providers.base import LLM, STT, TTS, AudioChunk, Transcript


@dataclass(frozen=True, slots=True)
class VoiceReply:
    """The full result of one turn through the pipeline."""

    transcript: Transcript
    reply_text: str
    audio: AudioChunk


class VoiceAgent:
    """End-to-end voice agent pipeline.

    Parameters
    ----------
    stt, tts, llm:
        The three providers. Use the offline fakes for local development and
        testing, or swap in real adapters in production.
    system_prompt:
        Seed instruction for the dialog manager.
    """

    def __init__(
        self,
        stt: STT,
        llm: LLM,
        tts: TTS,
        system_prompt: str = "You are a helpful, concise AI voice agent.",
    ) -> None:
        self.stt = stt
        self.tts = tts
        self.dialog = DialogManager(llm=llm, system_prompt=system_prompt)

    def handle_audio(self, audio: AudioChunk) -> VoiceReply:
        """Run one full turn starting from inbound caller audio."""
        transcript = self.stt.transcribe(audio)
        return self._respond_to_text(transcript.text, transcript)

    def handle_text(self, text: str) -> VoiceReply:
        """Run one full turn starting from already-transcribed text.

        Useful for text-simulated conversations and webhooks that deliver a
        speech transcript rather than raw audio.
        """
        transcript = Transcript(text=text, confidence=1.0, is_final=True)
        return self._respond_to_text(text, transcript)

    def _respond_to_text(self, text: str, transcript: Transcript) -> VoiceReply:
        self.dialog.add_user_turn(text)
        agent_turn = self.dialog.respond()
        audio = self.tts.synthesize(agent_turn.text)
        return VoiceReply(transcript=transcript, reply_text=agent_turn.text, audio=audio)
