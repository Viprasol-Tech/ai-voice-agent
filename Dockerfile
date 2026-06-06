# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install the package (with telephony extra so the webhook server is available).
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir ".[twilio]"

# Run as a non-root user.
RUN useradd --create-home --uid 1000 appuser
USER appuser

ENTRYPOINT ["ai-voice-agent"]
CMD ["--help"]
