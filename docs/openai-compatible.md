# OpenAI-Compatible Model Setup

Redbot sends requests to the standard chat-completions endpoint:

```text
POST {REDBOT_BASE_URL}/chat/completions
```

Required environment variables:

```bash
REDBOT_API_KEY=sk-your-key
REDBOT_BASE_URL=https://api.openai.com/v1
REDBOT_MODEL=gpt-4o-mini
```

You can point `REDBOT_BASE_URL` at:

- OpenAI official API;
- OpenRouter;
- a self-hosted model gateway;
- a local OpenAI-compatible server;
- any provider that exposes `/v1/chat/completions`.

Example:

```bash
redbot run research-brief \
  --topic "AI Agent 开源项目趋势" \
  --audience "科技博主" \
  --context "总结实际落地风险和下一步动作"
```

Use `--demo` when you want to test Redbot without any API key:

```bash
redbot run short-video-script \
  --topic "Claude vs GPT" \
  --audience "工程团队" \
  --context "比较模型在内部工具中的适用场景" \
  --demo
```
