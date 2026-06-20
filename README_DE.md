<div align="center">

# Redbot

### Ein lokal ausgerichteter KI-Ausführungsassistent für Creator, Operatoren und kleine Teams

[![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)
[![CI](https://github.com/RedStringAI/Redbot/actions/workflows/ci.yml/badge.svg)](https://github.com/RedStringAI/Redbot/actions/workflows/ci.yml)
[![OpenAI Compatible](https://img.shields.io/badge/API-OpenAI--compatible-111827.svg)](docs/openai-compatible.md)

### Official Repository: **[github.com/RedStringAI/Redbot](https://github.com/RedStringAI/Redbot)**

[English](README.md) | [中文](README_ZH.md) | [日本語](README_JA.md) | Deutsch | [FluxToken](docs/fluxtoken.md)

</div>

## Sponsor

<details open>
<summary>Recommended OpenAI-compatible gateway</summary>

Redbot ist provider-neutral. Jede OpenAI-compatible endpoint kann genutzt werden: OpenAI, FluxToken, OpenRouter, ein selbst gehostetes New API, lokale Modellserver oder andere kompatible Relays.

[FluxToken](https://fluxtoken.ai) ist ein Multi-Modell-API-Gateway für Mainstream-Modelle wie Claude und GPT. Es bietet einheitliche API Keys, Guthabenverwaltung, Nutzungslogs und Routing und eignet sich gut für Redbot-Demos und Creator-Workflows.

```powershell
$env:REDBOT_API_KEY="ft-your-key"
$env:REDBOT_BASE_URL="https://fluxtoken.ai/v1"
$env:REDBOT_MODEL="gpt-4o-mini"
```

</details>

## Overview

Redbot turns repeatable knowledge work into transparent task runs. Instead of starting from a blank chat, you use practical templates for research briefs, short-video scripts, content tables, weekly reports, and GitHub README drafts.

## Features

- Template-first execution for creator, office, and developer workflows.
- OpenAI-compatible model configuration.
- Local artifacts and JSON traces for every run.
- Local browser console and HTTP server.
- Feishu, Enterprise WeChat, WeChat official account, and generic webhook adapters.
- SQLite memory and a lightweight local knowledge base.
- MIT license for forks, tutorials, and community remixing.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
redbot templates
redbot run short-video-script --topic "Claude vs GPT" --audience "Douyin tech audience" --context "60-second comparison" --demo
```

Start the local console:

```bash
redbot desktop --demo --port 8765
```

Open:

```text
http://127.0.0.1:8765
```

## Built-In Templates

| Template | Output |
|---|---|
| `research-brief` | Topic research with angles, risks, and next actions |
| `short-video-script` | Short-video script with hook and structure |
| `content-table` | Turns messy notes into a table |
| `weekly-report` | Creates a clear weekly update |
| `github-readme` | Drafts a README for an open-source project |

## Documentation

- [OpenAI-compatible setup](docs/openai-compatible.md)
- [FluxToken setup](docs/fluxtoken.md)
- [Local client](docs/local-client.md)
- [Channel setup](docs/channels.md)
- [Product plan](docs/product.md)

## License

Redbot is released under the MIT License. See [LICENSE](LICENSE).

## Acknowledgements

Redbot is inspired by [HKUDS/nanobot](https://github.com/HKUDS/nanobot), an MIT-licensed lightweight personal AI agent project.
