from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from redbot.llm import LLMClient
from redbot.templates import TaskTemplate


@dataclass(frozen=True)
class TaskResult:
    task_id: str
    template_id: str
    artifact_path: Path
    trace_path: Path
    output: str


class RedbotRunner:
    def __init__(self, llm: LLMClient, workspace: str | Path = "redbot_workspace"):
        self.llm = llm
        self.workspace = Path(workspace)

    def run(self, template: TaskTemplate, topic: str, audience: str, context: str) -> TaskResult:
        return asyncio.run(self.run_async(template, topic, audience, context))

    async def run_async(
        self, template: TaskTemplate, topic: str, audience: str, context: str
    ) -> TaskResult:
        prompt = template.build_prompt(topic=topic, audience=audience, context=context)
        output = await self.llm.complete(prompt)
        task_id = self._task_id()
        artifact_path = self._artifact_path(task_id, topic)
        trace_path = self._trace_path(task_id)
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        trace_path.parent.mkdir(parents=True, exist_ok=True)

        artifact_path.write_text(output + "\n", encoding="utf-8")
        trace = {
            "task_id": task_id,
            "template_id": template.id,
            "template_name": template.name,
            "topic": topic,
            "audience": audience,
            "context": context,
            "artifact_path": str(artifact_path),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        trace_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return TaskResult(
            task_id=task_id,
            template_id=template.id,
            artifact_path=artifact_path,
            trace_path=trace_path,
            output=output,
        )

    def _artifact_path(self, task_id: str, topic: str) -> Path:
        return self.workspace / "artifacts" / f"{task_id}-{_slugify(topic)}.md"

    def _trace_path(self, task_id: str) -> Path:
        return self.workspace / "traces" / f"{task_id}.json"

    def _task_id(self) -> str:
        return f"redbot-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned[:64] or "task"
