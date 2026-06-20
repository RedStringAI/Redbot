# Channel Setup Notes

Redbot's channel adapters normalize chat messages into one internal call:

```text
channel + conversation_id + user_id + text -> LocalRedbotClient
```

The adapters are intentionally thin. Platform-specific authentication, public network exposure, and production hardening should be handled at the deployment edge.

## Feishu

Use Feishu Open Platform event subscriptions:

1. Create a Feishu app.
2. Enable bot capability.
3. Set the event request URL to:

```text
https://your-domain/webhook/feishu
```

4. Subscribe to text message events.
5. Add the bot to a group.

Redbot handles `url_verification` by returning the challenge. For text events, it reads the message text and returns a `redbot_reply` field for local testing. In production, you can extend the adapter to call Feishu's reply/send-message API.

Set this if you want Redbot to send replies through Feishu's message API:

```bash
REDBOT_FEISHU_ACCESS_TOKEN=tenant-or-bot-access-token
```

## Enterprise WeChat / 企业微信

There are two common routes:

- **Group robot webhook**: good for sending messages into a group.
- **Self-built app callback**: better for receiving messages and replying.

Redbot's `/webhook/wecom` accepts a normalized JSON payload:

```json
{
  "chatid": "group-1",
  "from": { "userid": "user-1" },
  "text": { "content": "/templates" }
}
```

It returns a markdown response payload:

```json
{
  "msgtype": "markdown",
  "markdown": { "content": "..." }
}
```

Set this if you want Redbot to push the reply into an Enterprise WeChat group robot:

```bash
REDBOT_WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...
```

## WeChat / 微信

For official WeChat accounts, configure the server callback:

```text
https://your-domain/webhook/wechat
```

Set:

```bash
REDBOT_WECHAT_TOKEN=your-token
```

Redbot verifies GET requests with the standard `signature`, `timestamp`, `nonce`, and `echostr` flow. Text messages are parsed from XML and answered with XML.

## Generic WeChat Bot Bridge

If you use a personal-WeChat bot framework or a bridge service, call:

```text
POST /webhook/generic
```

Payload:

```json
{
  "channel": "wechat-bridge",
  "conversation_id": "group-or-room",
  "user_id": "sender",
  "text": "/run weekly-report 本周项目进展"
}
```

This keeps Redbot open-source and provider-neutral without hard-coding one unofficial WeChat protocol.
