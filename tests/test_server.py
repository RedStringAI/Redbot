import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from redbot.server import RedbotLocalApp


class ServerTests(unittest.TestCase):
    def test_home_route_returns_local_console_html(self):
        with TemporaryDirectory() as tmp:
            app = RedbotLocalApp(workspace=Path(tmp), demo=True)

            status, headers, body = app.handle_text_route("GET", "/")

            self.assertEqual(status, 200)
            self.assertEqual(headers["content-type"], "text/html; charset=utf-8")
            self.assertIn("Redbot Local Client", body)
            self.assertIn("/api/chat", body)

    def test_local_chat_api_returns_response_dict(self):
        with TemporaryDirectory() as tmp:
            app = RedbotLocalApp(workspace=Path(tmp), demo=True)

            status, headers, body = app.handle_json_route(
                "POST",
                "/api/chat",
                {
                    "channel": "local",
                    "conversation_id": "room",
                    "user_id": "user",
                    "text": "/templates",
                },
            )

            self.assertEqual(status, 200)
            self.assertEqual(headers["content-type"], "application/json; charset=utf-8")
            self.assertIn("research-brief", json.loads(body)["reply"])

    def test_health_route_reports_enabled_channels(self):
        with TemporaryDirectory() as tmp:
            app = RedbotLocalApp(workspace=Path(tmp), demo=True)

            status, _, body = app.handle_json_route("GET", "/health", None)

            self.assertEqual(status, 200)
            self.assertEqual(json.loads(body)["channels"], ["feishu", "wecom", "wechat", "generic"])


if __name__ == "__main__":
    unittest.main()
