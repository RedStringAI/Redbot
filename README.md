<div align="center">

# Redbot

### A local-first AI execution assistant for creators, operators, and small teams

[![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)
[![CI](https://github.com/RedStringAI/Redbot/actions/workflows/ci.yml/badge.svg)](https://github.com/RedStringAI/Redbot/actions/workflows/ci.yml)
[![OpenAI Compatible](https://img.shields.io/badge/API-OpenAI--compatible-111827.svg)](docs/openai-compatible.md)
[![Local First](https://img.shields.io/badge/runtime-local--first-red.svg)](docs/local-client.md)

### Official Repository: **[github.com/RedStringAI/Redbot](https://github.com/RedStringAI/Redbot)**

English | [中文](README_ZH.md) | [日本語](README_JA.md) | [Deutsch](README_DE.md) | [FluxToken](docs/fluxtoken.md)

</div>

## Sponsor

<details open>
<summary>Recommended OpenAI-compatible gateway</summary>

<table>
<tr>
<td width="180"><strong>FluxToken</strong><br><a href="https://fluxtoken.ai">fluxtoken.ai</a></td>
<td>
Redbot works with any OpenAI-compatible endpoint. If you want a ready-to-use model gateway for demos, creator workflows, and Claude/GPT experiments, <a href="https://fluxtoken.ai">FluxToken</a> provides a multi-model API gateway with unified keys, balance management, usage logs, and routing across mainstream model providers. Set <code>REDBOT_BASE_URL=https://fluxtoken.ai/v1</code>, paste your FluxToken API key, and Redbot can run the same templates through your gateway.
<br><br>
Redbot stays provider-neutral: OpenAI, OpenRouter, local servers, self-hosted New API, and other compatible relays all work the same way.
</td>
</tr>
</table>

</details>

## Why Redbot

Redbot turns repeatable knowledge work into transparent task runs. Instead of opening a blank chat every time, you start from templates such as research briefs, short-video scripts, content tables, weekly reports, and GitHub README drafts.

- **Template-first execution**: built-in workflows for creators, operators, and developers.
- **OpenAI-compatible by default**: use OpenAI, FluxToken, OpenRouter, self-hosted gateways, or local model servers.
- **Local artifacts and traces**: every run writes the final output and a JSON trace you can inspect.
- **Chat-platform ready**: local endpoints for Feishu, Enterprise WeChat, WeChat official account callbacks, and generic bridges.
- **Memory and knowledge base**: SQLite-backed scoped memory plus keyword search over local `.md` and `.txt` files.
- **MIT open source**: easy to fork, teach, remix, and use in vibecoding videos.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
redbot templates
redbot run short-video-script --topic "Claude vs GPT" --audience "Douyin tech audience" --context "60-second model comparison" --demo
```

Start the local desktop-style console:

```bash
redbot desktop --demo --port 8765
```

Open:

```text
http://127.0.0.1:8765
```

## Use A Real Model

Redbot sends chat requests to:

```text
POST {REDBOT_BASE_URL}/chat/completions
```

OpenAI example:

```powershell
$env:REDBOT_API_KEY="sk-your-key"
$env:REDBOT_BASE_URL="https://api.openai.com/v1"
$env:REDBOT_MODEL="gpt-4o-mini"
```

FluxToken example:

```powershell
$env:REDBOT_API_KEY="ft-your-key"
$env:REDBOT_BASE_URL="https://fluxtoken.ai/v1"
$env:REDBOT_MODEL="gpt-4o-mini"
```

Then run:

```bash
redbot run research-brief --topic "Open-source AI agent trends" --audience "tech creator" --context "Find GitHub projects worth remixing"
```

More details: [OpenAI-compatible setup](docs/openai-compatible.md) and [FluxToken setup](docs/fluxtoken.md).

## Built-In Templates

| Template | Output |
|---|---|
| `research-brief` | Structured topic research with angles, risks, and next actions |
| `short-video-script` | Douyin/Xiaohongshu-style short-video script with a strong hook |
| `content-table` | Converts messy notes into a publishable table |
| `weekly-report` | Turns progress notes into a clear team update |
| `github-readme` | Drafts a GitHub README for a productized open-source project |

## Local Client

Redbot can run as a small local HTTP client:

```bash
redbot serve --demo --port 8765
```

Useful local commands:

```text
/templates
/run short-video-script Claude and GPT model comparison
/remember style=make output suitable for Douyin
/memory
/kb add Feishu setup notes
/kb search Feishu
```

Webhook endpoints:

| Platform | Endpoint |
|---|---|
| Feishu | `/webhook/feishu` |
| Enterprise WeChat / WeCom | `/webhook/wecom` |
| WeChat official account | `/webhook/wechat` |
| Generic bot bridge | `/webhook/generic` |

See [Local client](docs/local-client.md) and [Channel setup](docs/channels.md).

## Knowledge Base

Import local notes:

```bash
redbot kb import ./docs --workspace redbot_workspace
```

Search from the console or any channel:

```text
/kb search model gateway
```

The first version is intentionally small and dependency-free: SQLite storage plus lightweight keyword search. It is designed to be readable enough for tutorials and easy enough for the community to extend.

## Roadmap

- More creator templates for Douyin, Xiaohongshu, Bilibili, and WeChat Official Accounts.
- Richer web console for choosing templates and viewing traces.
- Built-in web research tool.
- File ingestion for PDF, DOCX, and meeting notes.
- Scheduled recurring tasks.
- Optional embeddings and vector search while keeping the simple command interface.

## How It Differs From nanobot

[nanobot](https://github.com/HKUDS/nanobot) is a broad personal AI agent framework with WebUI, channels, tools, memory, MCP, automation, and deployment. Redbot is a focused product fork-in-spirit for lightweight creator and office execution:

- narrower first-run experience;
- Chinese creator and operator templates;
- local artifacts and traces as the main product surface;
- simple OpenAI-compatible configuration;
- a smaller codebase designed for vibecoding videos and community remixing.

## Development

Redbot's runtime uses only the Python standard library. Run tests with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## License

Redbot is released under the MIT License. See [LICENSE](LICENSE).

## Acknowledgements

Redbot is inspired by [HKUDS/nanobot](https://github.com/HKUDS/nanobot), an MIT-licensed lightweight personal AI agent project. See [NOTICE.md](NOTICE.md).
