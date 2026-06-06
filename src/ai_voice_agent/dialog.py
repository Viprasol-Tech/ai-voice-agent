"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Dialog management: conversation state and turn-taking.

:class:`DialogManager` owns the message history (including the system prompt),
records who spoke when, and drives the LLM for each assistant turn. It keeps the
:class:`STT`/:class:`TTS` stages out of the picture so it can be unit-tested in
isolation and reused outside the voice pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from ai_voice_agent.providers.base import LLM, LLMResponse, Message, Role


class Speaker(StrEnum):
    """Who currently holds the conversational floor."""

    USER = "user"
    AGENT = "agent"


@dataclass(frozen=True, slots=True)
class Turn:
    """A single recorded utterance in the conversation."""

    speaker: Speaker
    text: str


@dataclass
class DialogManager:
    """Tracks conversation history and produces assistant replies.

    Parameters
    ----------
    llm:
        The language model used to generate assistant turns.
    system_prompt:
        Optional system instruction seeded as the first message.
    max_turns:
        Soft cap on how many turns to keep in the LLM context window. The
        system prompt is always preserved.
    """

    llm: LLM
    system_prompt: str = "You are a helpful, concise AI voice agent."
    max_turns: int = 40
    history: list[Turn] = field(default_factory=list)
    _next_speaker: Speaker = Speaker.USER

    @property
    def next_speaker(self) -> Speaker:
        """Whose turn it is to speak next."""
        return self._next_speaker

    @property
    def turn_count(self) -> int:
        """Total number of recorded turns."""
        return len(self.history)

    def add_user_turn(self, text: str) -> Turn:
        """Record a user utterance and hand the floor to the agent."""
        if self._next_speaker is not Speaker.USER:
            msg = "It is the agent's turn to speak, not the user's."
            raise RuntimeError(msg)
        turn = Turn(speaker=Speaker.USER, text=text)
        self.history.append(turn)
        self._next_speaker = Speaker.AGENT
        return turn

    def respond(self) -> Turn:
        """Generate the agent's reply to the conversation so far.

        Returns the recorded agent :class:`Turn` and hands the floor back to
        the user.
        """
        if self._next_speaker is not Speaker.AGENT:
            msg = "It is the user's turn to speak, not the agent's."
            raise RuntimeError(msg)
        response: LLMResponse = self.llm.complete(self._build_messages())
        turn = Turn(speaker=Speaker.AGENT, text=response.text)
        self.history.append(turn)
        self._next_speaker = Speaker.USER
        return turn

    def reset(self) -> None:
        """Clear history and return the floor to the user."""
        self.history.clear()
        self._next_speaker = Speaker.USER

    def _build_messages(self) -> list[Message]:
        messages: list[Message] = [Message(role="system", content=self.system_prompt)]
        recent = self.history[-self.max_turns :]
        for turn in recent:
            role: Role = "user" if turn.speaker is Speaker.USER else "assistant"
            messages.append(Message(role=role, content=turn.text))
        return messages
