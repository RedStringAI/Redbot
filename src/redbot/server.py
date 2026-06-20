from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from redbot.channels import FeishuAdapter, FeishuSender, WeChatAdapter, WeComAdapter, WeComRobotSender
from redbot.client import LocalRedbotClient
from redbot.llm import DemoLLMClient, LLMConfig, OpenAICompatibleClient
from redbot.store import RedbotStore


class RedbotLocalApp:
    def __init__(self, workspace: str | Path = "redbot_workspace", demo: bool = False):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        store = RedbotStore(self.workspace / "redbot.db")
        llm = DemoLLMClient() if demo else OpenAICompatibleClient(LLMConfig.from_env())
        self.client = LocalRedbotClient(store=store, llm=llm, workspace=self.workspace)
        self.feishu = FeishuAdapter(self.client, sender=FeishuSender())
        self.wecom = WeComAdapter(self.client, sender=WeComRobotSender())
        self.wechat = WeChatAdapter(self.client, token=_env_or_default("REDBOT_WECHAT_TOKEN", "redbot"))

    def handle_json_route(
        self, method: str, path: str, payload: dict | None
    ) -> tuple[int, dict[str, str], str]:
        if method == "GET" and path == "/health":
            return _json_response(
                {
                    "ok": True,
                    "channels": ["feishu", "wecom", "wechat", "generic"],
                }
            )
        if method == "POST" and path == "/api/chat":
            payload = payload or {}
            response = self.client.handle_text(
                payload.get("channel", "local"),
                payload.get("conversation_id", "local"),
                payload.get("user_id", "user"),
                payload.get("text", ""),
            )
            return _json_response({"reply": response.text})
        if method == "POST" and path == "/webhook/feishu":
            return _json_response(self.feishu.handle_json(payload or {}))
        if method == "POST" and path == "/webhook/wecom":
            return _json_response(self.wecom.handle_json(payload or {}))
        if method == "POST" and path == "/webhook/generic":
            payload = payload or {}
            response = self.client.handle_text(
                payload.get("channel", "generic"),
                payload.get("conversation_id", "generic"),
                payload.get("user_id", "user"),
                payload.get("text", ""),
            )
            return _json_response({"reply": response.text})
        return _json_response({"error": "not found"}, status=404)

    def handle_text_route(self, method: str, path: str) -> tuple[int, dict[str, str], str]:
        if method == "GET" and path == "/":
            return 200, {"content-type": "text/html; charset=utf-8"}, _console_html()
        return 404, {"content-type": "text/plain; charset=utf-8"}, "not found"


def serve(host: str = "127.0.0.1", port: int = 8765, workspace: str = "redbot_workspace", demo: bool = False) -> None:
    app = RedbotLocalApp(workspace=workspace, demo=demo)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path == "/":
                status, headers, body = app.handle_text_route("GET", parsed.path)
                _send(self, status, headers, body)
                return
            if parsed.path == "/webhook/wechat":
                query = parse_qs(parsed.query)
                try:
                    body = app.wechat.verify_get(
                        signature=query.get("signature", [""])[0],
                        timestamp=query.get("timestamp", [""])[0],
                        nonce=query.get("nonce", [""])[0],
                        echostr=query.get("echostr", [""])[0],
                    )
                    _send(self, 200, {"content-type": "text/plain; charset=utf-8"}, body)
                except ValueError as exc:
                    _send(self, 403, {"content-type": "text/plain; charset=utf-8"}, str(exc))
                return
            status, headers, body = app.handle_json_route("GET", parsed.path, None)
            _send(self, status, headers, body)

        def do_POST(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            raw = self.rfile.read(int(self.headers.get("content-length", "0"))).decode("utf-8")
            if parsed.path == "/webhook/wechat":
                _send(
                    self,
                    200,
                    {"content-type": "application/xml; charset=utf-8"},
                    app.wechat.handle_xml(raw),
                )
                return
            payload = json.loads(raw or "{}")
            status, headers, body = app.handle_json_route("POST", parsed.path, payload)
            _send(self, status, headers, body)

        def log_message(self, format: str, *args) -> None:  # noqa: A002
            return

    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Redbot local client listening on http://{host}:{port}")
    print("Webhook endpoints: /webhook/feishu /webhook/wecom /webhook/wechat /webhook/generic")
    server.serve_forever()


def _json_response(payload: dict, status: int = 200) -> tuple[int, dict[str, str], str]:
    return status, {"content-type": "application/json; charset=utf-8"}, json.dumps(
        payload, ensure_ascii=False
    )


def _send(handler: BaseHTTPRequestHandler, status: int, headers: dict[str, str], body: str) -> None:
    data = body.encode("utf-8")
    handler.send_response(status)
    for key, value in headers.items():
        handler.send_header(key, value)
    handler.send_header("content-length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def _env_or_default(name: str, default: str) -> str:
    import os

    return os.getenv(name, default)


def _console_html() -> str:
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Redbot Local Client</title>
  <style>
    body { font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; background: #f7f7f8; color: #1f2328; }
    main { max-width: 880px; margin: 0 auto; padding: 40px 20px; }
    h1 { margin: 0 0 8px; font-size: 32px; }
    p { color: #57606a; }
    textarea, input { width: 100%; box-sizing: border-box; border: 1px solid #d0d7de; border-radius: 8px; padding: 12px; font-size: 15px; background: white; }
    textarea { min-height: 140px; resize: vertical; }
    button { margin-top: 12px; border: 0; border-radius: 8px; padding: 11px 16px; background: #cf222e; color: white; font-weight: 700; cursor: pointer; }
    pre { white-space: pre-wrap; background: #0d1117; color: #e6edf3; padding: 16px; border-radius: 8px; min-height: 160px; overflow: auto; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .card { background: white; border: 1px solid #d0d7de; border-radius: 8px; padding: 16px; }
    code { background: #f0f0f0; padding: 2px 5px; border-radius: 4px; }
  </style>
</head>
<body>
  <main>
    <h1>Redbot Local Client</h1>
    <p>本地 AI 执行助理，支持记忆、知识库、任务模板，以及飞书/企业微信/微信 webhook。</p>
    <div class="grid">
      <section class="card">
        <h2>发送消息</h2>
        <input id="conversation" value="local-room" aria-label="conversation">
        <textarea id="text">/templates</textarea>
        <button onclick="sendMessage()">发送到 /api/chat</button>
      </section>
      <section class="card">
        <h2>常用命令</h2>
        <p><code>/remember style=输出要适合抖音</code></p>
        <p><code>/kb add 标题\n内容</code></p>
        <p><code>/kb search 关键词</code></p>
        <p><code>/run short-video-script 主题</code></p>
      </section>
    </div>
    <h2>返回结果</h2>
    <pre id="output"></pre>
  </main>
  <script>
    async function sendMessage() {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          channel: 'local',
          conversation_id: document.getElementById('conversation').value,
          user_id: 'local-user',
          text: document.getElementById('text').value
        })
      });
      const data = await response.json();
      document.getElementById('output').textContent = data.reply || JSON.stringify(data, null, 2);
    }
  </script>
</body>
</html>"""
