import unittest

from redbot.templates import get_template, list_templates


class TemplateTests(unittest.TestCase):
    def test_lists_workflow_templates_with_marketable_names(self):
        templates = list_templates()

        self.assertEqual(
            [template.id for template in templates],
            [
                "research-brief",
                "short-video-script",
                "content-table",
                "weekly-report",
                "github-readme",
            ],
        )
        self.assertIn("深度研究", templates[0].name)

    def test_get_template_rejects_unknown_template_id(self):
        with self.assertRaisesRegex(KeyError, "Unknown Redbot template"):
            get_template("unknown")

    def test_template_builds_prompt_with_context_and_deliverable(self):
        template = get_template("short-video-script")

        prompt = template.build_prompt(
            topic="Claude 和 GPT 模型对比",
            audience="工程团队",
            context="模型来自 OpenAI-compatible API，需要自然提到可替换模型。",
        )

        self.assertIn("Claude 和 GPT 模型对比", prompt)
        self.assertIn("工程团队", prompt)
        self.assertIn("开头钩子", prompt)
        self.assertIn("模型来自 OpenAI-compatible API", prompt)


if __name__ == "__main__":
    unittest.main()
