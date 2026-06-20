# Redbot Local Client

Redbot can run as a local client server. It keeps your artifacts, traces, memory, and knowledge base on your own machine while exposing webhook entry points for chat platforms.

## Start

Demo mode, no model API key:

```bash
redbot serve --demo --port 8765
```

Real model mode:

```bash
set REDBOT_API_KEY=sk-your-key
set REDBOT_BASE_URL=https://your-openai-compatible-endpoint/v1
set REDBOT_MODEL=gpt-4o-mini
redbot serve --port 8765
```

Open the local console:

```text
http://127.0.0.1:8765
```

## Local API

```bash
curl -X POST http://127.0.0.1:8765/api/chat \
  -H "content-type: application/json" \
  -d '{"channel":"local","conversation_id":"room","user_id":"user","text":"/templates"}'
```

## Commands

```text
/templates
/run short-video-script Claude 和 GPT 模型对比
/remember style=输出要适合抖音
/memory
/kb add 飞书配置
飞书机器人需要事件订阅地址和回调 token。
/kb search 飞书
```

Import local `.md` and `.txt` files:

```bash
redbot kb import ./docs --workspace redbot_workspace
```

Then ask from the local console or any channel:

```text
/kb search 飞书
```

## Webhook Endpoints

| Platform | Endpoint | Notes |
|---|---|---|
| Feishu | `/webhook/feishu` | Handles URL verification and text message events. |
| WeCom / 企业微信 | `/webhook/wecom` | Accepts JSON text payloads and returns markdown payloads. |
| WeChat / 微信公众号 | `/webhook/wechat` | Supports GET token verification and XML text message callbacks. |
| Generic bridge | `/webhook/generic` | Use this with third-party WeChat bot bridges or custom scripts. |

For local testing, use a tunnel such as Cloudflare Tunnel, ngrok, or a server reverse proxy so Feishu/WeChat can reach your local webhook URL.

Optional outbound settings:

```bash
REDBOT_FEISHU_ACCESS_TOKEN=tenant-or-bot-access-token
REDBOT_WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...
```

If these are set, Redbot will try to send replies back to Feishu or Enterprise WeChat after handling the incoming message. If they are not set, Redbot still returns the reply in the local HTTP response for testing and bridge integrations.

## Memory

Memory is scoped by:

```text
channel:conversation_id:user_id
```

This lets Redbot remember different preferences for different groups and users.

## Knowledge Base

The MVP knowledge base stores documents in SQLite and performs lightweight keyword search. It is intentionally simple and dependency-free. A later version can add embeddings and vector search while keeping the same command interface.

## Data Location

By default, Redbot writes data to:

```text
redbot_workspace/
  redbot.db
  artifacts/
  traces/
```

Use `--workspace` to choose another folder.
