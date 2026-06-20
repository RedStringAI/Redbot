from __future__ import annotations

import hashlib
import json
import time
import xml.etree.ElementTree as ET
from html import escape

from redbot.client import LocalRedbotClient


class FeishuAdapter:
    def __init__(self, client: LocalRedbotClient | None):
        self.client = client

    def handle_json(self, payload: dict) -> dict:
        if payload.get("type") == "url_verification":
            return {"challenge": payload.get("challenge", "")}
        event = payload.get("event", {})
        message = event.get("message", {})
        if message.get("message_type") != "text" or self.client is None:
            return {"code": 0}
        content = json.loads(message.get("content", "{}")).get("text", "")
        sender = event.get("sender", {}).get("sender_id", {}).get("open_id", "unknown")
        chat_id = message.get("chat_id", "direct")
        reply = self.client.handle_text("feishu", chat_id, sender, content)
        return {"code": 0, "redbot_reply": reply.text}


class WeComAdapter:
    def __init__(self, client: LocalRedbotClient | None):
        self.client = client

    def handle_json(self, payload: dict) -> dict:
        text = payload.get("text", {}).get("content", "")
        chat_id = payload.get("chatid") or payload.get("conversation_id") or "wecom"
        user_id = payload.get("from", {}).get("userid") or payload.get("user_id") or "unknown"
        reply_text = ""
        if self.client is not None:
            reply_text = self.client.handle_text("wecom", chat_id, user_id, text).text
        return {"msgtype": "markdown", "markdown": {"content": reply_text}}


class WeChatAdapter:
    def __init__(self, client: LocalRedbotClient | None, token: str):
        self.client = client
        self.token = token

    def sign(self, timestamp: str, nonce: str) -> str:
        raw = "".join(sorted([self.token, timestamp, nonce]))
        return hashlib.sha1(raw.encode("utf-8")).hexdigest()

    def verify_get(self, signature: str, timestamp: str, nonce: str, echostr: str) -> str:
        if self.sign(timestamp, nonce) != signature:
            raise ValueError("Invalid WeChat signature")
        return echostr

    def handle_xml(self, xml_text: str) -> str:
        root = ET.fromstring(xml_text)
        to_user = _xml_text(root, "ToUserName")
        from_user = _xml_text(root, "FromUserName")
        content = _xml_text(root, "Content")
        reply = ""
        if self.client is not None:
            reply = self.client.handle_text("wechat", from_user, from_user, content).text
        return (
            "<xml>"
            f"<ToUserName><![CDATA[{escape(from_user)}]]></ToUserName>"
            f"<FromUserName><![CDATA[{escape(to_user)}]]></FromUserName>"
            f"<CreateTime>{int(time.time())}</CreateTime>"
            "<MsgType><![CDATA[text]]></MsgType>"
            f"<Content><![CDATA[{reply}]]></Content>"
            "</xml>"
        )


def _xml_text(root: ET.Element, tag: str) -> str:
    node = root.find(tag)
    return node.text if node is not None and node.text is not None else ""
