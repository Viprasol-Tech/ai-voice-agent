# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | ✅        |

## Reporting a vulnerability

If you discover a security vulnerability in **AI Voice Agent**, please report it
privately. **Do not open a public issue.**

- Email: [support@viprasol.com](mailto:support@viprasol.com)
- Subject: `SECURITY — ai-voice-agent`

Please include a description of the issue, steps to reproduce, and any relevant
logs or proof of concept. We aim to acknowledge reports within 72 hours and to
provide a remediation timeline after triage.

## Handling secrets

This project never requires API keys to run its offline fakes. When using the
optional ElevenLabs or Twilio adapters, keep credentials in environment
variables or a local `.env` file (which is git-ignored). Never commit `.env`,
`*.pem`, or `*.key` files.

Thank you for helping keep the Viprasol ecosystem and its users safe.
