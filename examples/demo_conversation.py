"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Runnable demo: a scripted, fully-offline voice conversation.

Run it with::

    python examples/demo_conversation.py

No network access or API keys are required — everything uses the deterministic
fake providers.
"""

from __future__ import annotations

from ai_voice_agent.agent import VoiceAgent
from ai_voice_agent.providers.fakes import FakeLLM, FakeSTT, FakeTTS


def main() -> None:
    agent = VoiceAgent(
        stt=FakeSTT(),
        llm=FakeLLM(name="Vira"),
        tts=FakeTTS(),
        system_prompt="You are Vira, a concise AI voice agent by Viprasol Tech.",
    )

    script = [
        "Hello!",
        "What is your name?",
        "Can you book me a demo next week?",
        "Thank you, goodbye.",
    ]

    print("=== AI Voice Agent demo (offline) ===\n")
    for line in script:
        reply = agent.handle_text(line)
        print(f"Caller : {line}")
        print(f"Vira   : {reply.reply_text}")
        print(f"         (synthesized {len(reply.audio)} bytes of audio)\n")

    print(f"Conversation finished after {agent.dialog.turn_count} turns.")


if __name__ == "__main__":
    main()
