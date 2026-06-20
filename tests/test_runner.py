import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from redbot.llm import DemoLLMClient
from redbot.runner import RedbotRunner
from redbot.templates import get_template


class RunnerTests(unittest.TestCase):
    def test_runner_creates_trace_and_artifact(self):
        with TemporaryDirectory() as tmp:
            runner = RedbotRunner(
                llm=DemoLLMClient(),
                workspace=tmp,
            )

            result = runner.run(
                template=get_template("research-brief"),
                topic="开源 AI Agent 工具趋势",
                audience="工程团队",
                context="关注 GitHub 开源项目、落地风险和下一步行动。",
            )

            self.assertTrue(result.task_id.startswith("redbot-"))
            self.assertEqual(result.template_id, "research-brief")
            self.assertTrue(result.artifact_path.exists())
            self.assertTrue(result.trace_path.exists())
            artifact = result.artifact_path.read_text(encoding="utf-8")
            trace = result.trace_path.read_text(encoding="utf-8")
            self.assertIn("开源 AI Agent 工具趋势", artifact)
            self.assertIn("Redbot demo response", artifact)
            self.assertIn('"template_id": "research-brief"', trace)

    def test_runner_uses_safe_slug_for_artifact_names(self):
        with TemporaryDirectory() as tmp:
            runner = RedbotRunner(llm=DemoLLMClient(), workspace=tmp)

            result = runner.run(
                template=get_template("github-readme"),
                topic="Redbot: Workflow Agent!",
                audience="GitHub visitors",
                context="Make it attractive.",
            )

            self.assertEqual(result.artifact_path.parent, Path(tmp) / "artifacts")
            self.assertIn("redbot-workflow-agent", result.artifact_path.name)

    def test_runner_uses_ascii_fallback_for_chinese_slug(self):
        with TemporaryDirectory() as tmp:
            runner = RedbotRunner(llm=DemoLLMClient(), workspace=tmp)

            result = runner.run(
                template=get_template("short-video-script"),
                topic="Claude 和 GPT 模型对比",
                audience="科技爱好者",
                context="避免 Windows 终端乱码。",
            )

            self.assertTrue(result.artifact_path.name.endswith("-claude-gpt.md"))


if __name__ == "__main__":
    unittest.main()
