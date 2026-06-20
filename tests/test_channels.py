import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from redbot.channels import FeishuAdapter, WeChatAdapter, WeComAdapter
from redbot.client import LocalRedbotClient
from redbot.llm import DemoLLMClient
from redbot.store import RedbotStore


def make_client(tmp):
    return LocalRedbotClient(
        store=RedbotStore(Path(tmp) / "redbot.db"),
        llm=DemoLLMClient(),
        workspace=tmp,
    )


class ChannelTests(unittest.TestCase):
    def test_feishu_url_verification_returns_challenge(self):
        adapter = FeishuAdapter(client=None)

        response = adapter.handle_json({"type": "url_verification", "challenge": "abc123"})

        self.assertEqual(response, {"challenge": "abc123"})

    def test_feishu_message_event_uses_unified_client(self):
        with TemporaryDirectory() as tmp:
            adapter = FeishuAdapter(client=make_client(tmp))

            response = adapter.handle_json(
                {
                    "event": {
                        "sender": {"sender_id": {"open_id": "ou-user"}},
                        "message": {
                            "chat_id": "oc-chat",
                            "message_type": "text",
                            "content": "{\"text\":\"/templates\"}",
                        },
                    }
                }
            )

            self.assertEqual(response["code"], 0)
            self.assertIn("research-brief", response["redbot_reply"])

    def test_wecom_json_message_returns_markdown_payload(self):
        with TemporaryDirectory() as tmp:
            adapter = WeComAdapter(client=make_client(tmp))

            response = adapter.handle_json(
                {
                    "chatid": "group-1",
                    "from": {"userid": "u1"},
                    "text": {"content": "/templates"},
                }
            )

            self.assertEqual(response["msgtype"], "markdown")
            self.assertIn("research-brief", response["markdown"]["content"])

    def test_wechat_get_verification_returns_echostr_when_signature_matches(self):
        adapter = WeChatAdapter(client=None, token="redbot-token")

        signature = adapter.sign(timestamp="1", nonce="2")
        response = adapter.verify_get(signature=signature, timestamp="1", nonce="2", echostr="ok")

        self.assertEqual(response, "ok")

    def test_wechat_xml_message_returns_text_xml(self):
        with TemporaryDirectory() as tmp:
            adapter = WeChatAdapter(client=make_client(tmp), token="redbot-token")
            xml = (
                "<xml><ToUserName><![CDATA[to]]></ToUserName>"
                "<FromUserName><![CDATA[from-user]]></FromUserName>"
                "<CreateTime>1</CreateTime><MsgType><![CDATA[text]]></MsgType>"
                "<Content><![CDATA[/templates]]></Content></xml>"
            )

            response = adapter.handle_xml(xml)

            self.assertIn("<MsgType><![CDATA[text]]></MsgType>", response)
            self.assertIn("research-brief", response)


if __name__ == "__main__":
    unittest.main()
