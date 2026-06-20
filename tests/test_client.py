import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from redbot.client import LocalRedbotClient
from redbot.llm import DemoLLMClient
from redbot.store import RedbotStore


class RecordingLLM:
    def __init__(self):
        self.prompts = []

    async def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return "模型输出"


class ClientTests(unittest.TestCase):
    def test_client_remembers_and_lists_memory(self):
        with TemporaryDirectory() as tmp:
            client = LocalRedbotClient(
                store=RedbotStore(Path(tmp) / "redbot.db"),
                llm=DemoLLMClient(),
                workspace=tmp,
            )

            saved = client.handle_text("feishu", "chat-1", "user-1", "/remember tone=说话像产品经理")
            listed = client.handle_text("feishu", "chat-1", "user-1", "/memory")

            self.assertIn("已记住", saved.text)
            self.assertIn("tone", listed.text)
            self.assertIn("说话像产品经理", listed.text)

    def test_client_adds_and_searches_knowledge(self):
        with TemporaryDirectory() as tmp:
            client = LocalRedbotClient(
                store=RedbotStore(Path(tmp) / "redbot.db"),
                llm=DemoLLMClient(),
                workspace=tmp,
            )

            added = client.handle_text(
                "local",
                "room",
                "user",
                "/kb add 飞书配置\n飞书机器人需要事件订阅地址和回调 token。",
            )
            found = client.handle_text("local", "room", "user", "/kb search 事件订阅")

            self.assertIn("已加入知识库", added.text)
            self.assertIn("飞书配置", found.text)
            self.assertIn("事件订阅", found.text)

    def test_run_command_injects_memory_and_knowledge_context(self):
        with TemporaryDirectory() as tmp:
            llm = RecordingLLM()
            client = LocalRedbotClient(
                store=RedbotStore(Path(tmp) / "redbot.db"),
                llm=llm,
                workspace=tmp,
            )
            client.handle_text("local", "room", "user", "/remember style=输出要适合抖音")
            client.handle_text("local", "room", "user", "/kb add 模型资料\nClaude 适合长文推理。")

            response = client.handle_text(
                "local",
                "room",
                "user",
                "/run short-video-script Claude 和 GPT 模型对比",
            )

            self.assertIn("Artifact", response.text)
            self.assertIn("输出要适合抖音", llm.prompts[0])
            self.assertIn("Claude 适合长文推理", llm.prompts[0])


if __name__ == "__main__":
    unittest.main()
