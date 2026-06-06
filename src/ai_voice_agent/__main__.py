"""Part of AI Voice Agent by Viprasol Tech Private Limited (https://viprasol.com).

Allow ``python -m ai_voice_agent`` to launch the CLI.
"""

from __future__ import annotations

import sys

from ai_voice_agent.cli import main

if __name__ == "__main__":
    sys.exit(main())
