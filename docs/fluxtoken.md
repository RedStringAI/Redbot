# FluxToken Setup

Redbot is provider-neutral and works with any OpenAI-compatible endpoint. FluxToken is one recommended gateway when you want a ready model relay for production testing, document workflows, and Claude/GPT experiments.

## What FluxToken Provides

FluxToken is based on a multi-model API gateway pattern:

- unified API keys for compatible clients;
- model routing across mainstream upstream providers;
- support for Claude, GPT, Gemini, Azure, AWS Bedrock, and other model families through gateway adapters;
- user management, balance/quota tracking, billing records, and usage logs;
- a web console at [fluxtoken.ai](https://fluxtoken.ai);
- an Open WebUI-style chat entry at [chat.fluxtoken.ai](https://chat.fluxtoken.ai).

Redbot only needs the OpenAI-compatible API URL and a key. It does not require FluxToken-specific code.

## Environment Variables

PowerShell:

```powershell
$env:REDBOT_API_KEY="ft-your-key"
$env:REDBOT_BASE_URL="https://fluxtoken.ai/v1"
$env:REDBOT_MODEL="gpt-4o-mini"
```

Command Prompt:

```bat
set REDBOT_API_KEY=ft-your-key
set REDBOT_BASE_URL=https://fluxtoken.ai/v1
set REDBOT_MODEL=gpt-4o-mini
```

Linux/macOS:

```bash
export REDBOT_API_KEY=ft-your-key
export REDBOT_BASE_URL=https://fluxtoken.ai/v1
export REDBOT_MODEL=gpt-4o-mini
```

## Run Redbot

```bash
redbot run research-brief \
  --topic "Open-source AI agent projects" \
  --audience "engineering team" \
  --context "Summarize practical adoption risks and next actions"
```

For local console mode:

```bash
redbot desktop --port 8765
```

Then open:

```text
http://127.0.0.1:8765
```

## Provider-Neutral Fallback

If you use another compatible provider, keep the same Redbot commands and only replace:

```text
REDBOT_API_KEY
REDBOT_BASE_URL
REDBOT_MODEL
```

Examples:

```text
https://api.openai.com/v1
https://openrouter.ai/api/v1
https://your-new-api-domain.example/v1
http://127.0.0.1:11434/v1
```

## Notes For Public Demos

- Do not show real API keys in screenshots or videos.
- Use `--demo` when testing setup flows without a model key.
- If a model call fails, check the gateway balance, key permissions, selected model name, and usage logs first.
- Keep Redbot provider-neutral in public documentation; present FluxToken as one convenient backend option.
