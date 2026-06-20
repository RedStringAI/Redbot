# Redbot

Redbot is an open-source personal AI execution assistant for creators, operators, and small teams. It turns repeatable knowledge work into transparent task runs: research briefs, short-video scripts, content tables, weekly reports, and GitHub README drafts.

It is inspired by the lightweight personal-agent direction of [nanobot](https://github.com/HKUDS/nanobot), but Redbot's first product surface is intentionally narrower: Chinese creator and office workflows, OpenAI-compatible model endpoints, readable traces, and reusable task templates.

## Why Redbot

- **Task templates, not blank chat**: start from real creator and office deliverables.
- **OpenAI-compatible by default**: use OpenAI, OpenRouter, local gateways, or your own model relay.
- **Traceable execution**: every run writes the final artifact and a JSON trace.
- **MIT open source**: easy to fork, teach, remix, and deploy.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
redbot templates
redbot run short-video-script --topic "Claude vs GPT" --audience "抖音科技爱好者" --context "做一个 60 秒模型对比视频" --demo
```

Start the local desktop client:

```bash
redbot desktop --demo --port 8765
```

Then open:

```text
http://127.0.0.1:8765
```

Import local notes into the knowledge base:

```bash
redbot kb import ./docs
```

Use a real model through any OpenAI-compatible endpoint:

```bash
set REDBOT_API_KEY=sk-your-key
set REDBOT_BASE_URL=https://api.openai.com/v1
set REDBOT_MODEL=gpt-4o-mini

redbot run research-brief --topic "开源 AI Agent 趋势" --audience "科技博主" --context "关注 GitHub 二创机会"
```

PowerShell:

```powershell
$env:REDBOT_API_KEY="sk-your-key"
$env:REDBOT_BASE_URL="https://api.openai.com/v1"
$env:REDBOT_MODEL="gpt-4o-mini"
```

## Built-In Templates

| Template | Output |
|---|---|
| `research-brief` | Structured topic research with angles, risks, and next actions |
| `short-video-script` | Douyin/Xiaohongshu-style short-video script with a strong hook |
| `content-table` | Extracts messy notes into a publishable table |
| `weekly-report` | Converts progress notes into a clear weekly report |
| `github-readme` | Drafts a GitHub README for a productized open-source project |

## Product Direction

Redbot is meant to become a practical personal execution assistant:

1. Creator workflows: topic research, script writing, cover-copy ideas, publishing checklists.
2. Office workflows: weekly reports, meeting summaries, project update drafts.
3. Developer workflows: README, changelog, issue triage, release notes.
4. Local client workflows: Feishu group entry, Enterprise WeChat group entry, WeChat-compatible webhook entry, memory, and knowledge base.
5. Transparent automation: artifacts and traces are local files that can be inspected and shared.

More detail:

- [Product plan](docs/product.md)
- [OpenAI-compatible setup](docs/openai-compatible.md)
- [Local client](docs/local-client.md)
- [Channel setup](docs/channels.md)
- [Douyin series ideas](docs/douyin-series.md)

## Development

Redbot's runtime uses only the Python standard library. Run tests with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## How It Differs From nanobot

nanobot is a broad personal AI agent framework with WebUI, channels, tools, memory, MCP, automation, and deployment. Redbot is a focused product fork-in-spirit for lightweight creator/office execution:

- narrower first-run experience;
- Chinese creator and operator templates;
- local artifacts and traces as the main product surface;
- simple OpenAI-compatible configuration;
- a smaller codebase designed for vibecoding videos and community remixing.

## License

Redbot is released under the MIT License. See [LICENSE](LICENSE).

## Acknowledgements

Redbot is inspired by [HKUDS/nanobot](https://github.com/HKUDS/nanobot), an MIT-licensed lightweight personal AI agent project. See [NOTICE.md](NOTICE.md).
