from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from redbot.llm import LLMClient
from redbot.runner import RedbotRunner
from redbot.store import RedbotStore
from redbot.templates import get_template, list_templates


@dataclass(frozen=True)
class ClientResponse:
    text: str


class LocalRedbotClient:
    def __init__(self, store: RedbotStore, llm: LLMClient, workspace: str | Path):
        self.store = store
        self.llm = llm
        self.workspace = Path(workspace)

    def handle_text(
        self,
        channel: str,
        conversation_id: str,
        user_id: str,
        text: str,
    ) -> ClientResponse:
        self.store.record_message(channel, conversation_id, user_id, text, direction="in")
        scope = f"{channel}:{conversation_id}:{user_id}"
        try:
            response = self._handle_command(scope, text.strip())
        except Exception as exc:  # pragma: no cover - safety net for webhook callers
            response = ClientResponse(f"Redbot 执行失败: {exc}")
        self.store.record_message(channel, conversation_id, "redbot", response.text, direction="out")
        return response

    def _handle_command(self, scope: str, text: str) -> ClientResponse:
        if text in {"/help", "help", ""}:
            return ClientResponse(_help_text())
        if text == "/templates":
            lines = [f"- {template.id}: {template.name}" for template in list_templates()]
            return ClientResponse("Redbot 可用模板:\n" + "\n".join(lines))
        if text.startswith("/remember "):
            return self._remember(scope, text.removeprefix("/remember ").strip())
        if text == "/memory":
            memories = self.store.list_memories(scope)
            if not memories:
                return ClientResponse("当前会话还没有记忆。")
            lines = [f"- {key}: {value}" for key, value in memories.items()]
            return ClientResponse("当前记忆:\n" + "\n".join(lines))
        if text.startswith("/kb add "):
            return self._add_knowledge(text.removeprefix("/kb add ").strip())
        if text.startswith("/kb search "):
            return self._search_knowledge(text.removeprefix("/kb search ").strip())
        if text.startswith("/run "):
            return self._run_task(scope, text.removeprefix("/run ").strip())
        return ClientResponse("我收到啦。发送 /help 查看 Redbot 支持的命令。")

    def _remember(self, scope: str, payload: str) -> ClientResponse:
        if "=" not in payload:
            return ClientResponse("用法: /remember key=value")
        key, value = payload.split("=", 1)
        self.store.save_memory(scope, key=key, value=value)
        return ClientResponse(f"已记住: {key.strip()} = {value.strip()}")

    def _add_knowledge(self, payload: str) -> ClientResponse:
        title, content = _split_title_content(payload)
        doc_id = self.store.add_document(title=title, content=content, source="chat")
        return ClientResponse(f"已加入知识库 #{doc_id}: {title}")

    def _search_knowledge(self, query: str) -> ClientResponse:
        hits = self.store.search_knowledge(query, limit=5)
        if not hits:
            return ClientResponse("知识库没有找到相关内容。")
        lines = [f"- {hit.title}: {hit.content[:160]}" for hit in hits]
        return ClientResponse("知识库命中:\n" + "\n".join(lines))

    def _run_task(self, scope: str, payload: str) -> ClientResponse:
        parts = payload.split(maxsplit=1)
        if len(parts) != 2:
            return ClientResponse("用法: /run <template_id> <topic>")
        template_id, topic = parts
        template = get_template(template_id)
        memories = self.store.list_memories(scope)
        knowledge_hits = self.store.search_knowledge(topic, limit=3)
        context = _context_from_memory_and_knowledge(memories, knowledge_hits)
        result = RedbotRunner(llm=self.llm, workspace=self.workspace).run(
            template=template,
            topic=topic,
            audience="当前群聊或用户",
            context=context,
        )
        return ClientResponse(
            f"Redbot 已完成 {template.name}\n"
            f"Artifact: {result.artifact_path}\n"
            f"Trace: {result.trace_path}\n\n"
            f"{result.output[:1200]}"
        )


def _split_title_content(payload: str) -> tuple[str, str]:
    lines = [line.strip() for line in payload.splitlines() if line.strip()]
    if not lines:
        return "未命名资料", ""
    if len(lines) == 1:
        return lines[0][:40], lines[0]
    return lines[0], "\n".join(lines[1:])


def _context_from_memory_and_knowledge(memories: dict[str, str], hits: list) -> str:
    blocks = []
    if memories:
        blocks.append("用户/会话记忆:\n" + "\n".join(f"- {k}: {v}" for k, v in memories.items()))
    if hits:
        blocks.append("知识库相关资料:\n" + "\n".join(f"- {hit.title}: {hit.content}" for hit in hits))
    return "\n\n".join(blocks) or "无额外背景。"


def _help_text() -> str:
    return (
        "Redbot 本地客户端命令:\n"
        "- /templates 查看任务模板\n"
        "- /run <template_id> <topic> 执行任务\n"
        "- /remember key=value 保存当前用户记忆\n"
        "- /memory 查看当前用户记忆\n"
        "- /kb add 标题\\n内容 加入知识库\n"
        "- /kb search 关键词 搜索知识库"
    )
