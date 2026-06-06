"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

A tiny command-line REPL that simulates a voice conversation entirely in text,
using the offline fakes. Run it with::

    python -m ai_voice_agent

or, after installation, via the ``ai-voice-agent`` console script.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from ai_voice_agent import __version__
from ai_voice_agent.agent import VoiceAgent
from ai_voice_agent.providers.fakes import FakeLLM, FakeSTT, FakeTTS


def build_default_agent(agent_name: str = "Vira") -> VoiceAgent:
    """Create a fully-offline :class:`VoiceAgent` backed by the fakes."""
    return VoiceAgent(
        stt=FakeSTT(),
        llm=FakeLLM(name=agent_name),
        tts=FakeTTS(),
        system_prompt=f"You are {agent_name}, a concise AI voice agent by Viprasol Tech.",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for the ``ai-voice-agent`` console script."""
    parser = argparse.ArgumentParser(
        prog="ai-voice-agent",
        description="Text-simulated AI voice agent conversation (offline).",
    )
    parser.add_argument("--name", default="Vira", help="Agent name (default: Vira).")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--say",
        action="append",
        default=None,
        metavar="TEXT",
        help="Send one scripted line and print the reply; repeatable. "
        "If omitted, an interactive REPL starts.",
    )
    args = parser.parse_args(argv)

    agent = build_default_agent(agent_name=args.name)

    if args.say:
        for line in args.say:
            reply = agent.handle_text(line)
            print(f"You: {line}")
            print(f"{args.name}: {reply.reply_text}")
        return 0

    print(f"AI Voice Agent v{__version__} — type 'quit' to exit.")
    print(f"{args.name} is ready. Say hello!\n")
    while True:
        try:
            line = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.lower() in {"quit", "exit"}:
            break
        if not line:
            continue
        reply = agent.handle_text(line)
        print(f"{args.name}: {reply.reply_text}  [{len(reply.audio)} bytes of audio]\n")

    print("Goodbye!")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
