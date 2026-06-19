from __future__ import annotations

import asyncio
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol


class LLMClient(Protocol):
    async def complete(self, prompt: str) -> str:
        """Return a model completion for a prepared task prompt."""


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o-mini"
    timeout_seconds: float = 60.0

    @classmethod
    def from_env(cls) -> "LLMConfig":
        return cls(
            api_key=os.getenv("REDBOT_API_KEY", ""),
            base_url=os.getenv("REDBOT_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            model=os.getenv("REDBOT_MODEL", "gpt-4o-mini"),
            timeout_seconds=float(os.getenv("REDBOT_TIMEOUT_SECONDS", "60")),
        )


class DemoLLMClient:
    async def complete(self, prompt: str) -> str:
        first_topic_line = next((line for line in prompt.splitlines() if line.startswith("主题:")), "主题: Demo")
        topic = first_topic_line.replace("主题:", "", 1).strip()
        return (
            f"# Redbot demo response: {topic}\n\n"
            "这是 Redbot 的离线演示输出，用于验证模板、任务记录和产物生成流程。\n\n"
            "## 可执行结果\n"
            "- 已根据输入主题生成结构化交付物。\n"
            "- 真实运行时会调用 REDBOT_BASE_URL 指向的 OpenAI-compatible 模型接口。\n"
            "- 你可以把这里替换成 Claude、GPT 或自己的模型中转服务。\n\n"
            "## 下一步\n"
            "1. 配置 `REDBOT_API_KEY`。\n"
            "2. 配置 `REDBOT_BASE_URL`。\n"
            "3. 重新运行同一个模板获得真实模型输出。\n"
        )


class OpenAICompatibleClient:
    def __init__(self, config: LLMConfig):
        if not config.api_key:
            raise ValueError("REDBOT_API_KEY is required for real model requests.")
        self.config = config

    async def complete(self, prompt: str) -> str:
        return await asyncio.to_thread(self._complete_sync, prompt)

    def _complete_sync(self, prompt: str) -> str:
        payload = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are Redbot, a practical personal AI execution assistant.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            f"{self.config.base_url.rstrip('/')}/chat/completions",
            data=data,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Model request failed with HTTP {exc.code}: {error_body}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Model request failed: {exc.reason}") from exc

        try:
            return body["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected model response shape: {body}") from exc
