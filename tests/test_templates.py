import unittest

from redbot.templates import get_template, list_templates


class TemplateTests(unittest.TestCase):
    def test_lists_creator_templates_with_marketable_names(self):
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
            audience="抖音科技爱好者",
            context="模型来自 OpenAI-compatible API，视频要自然提到可替换模型。",
        )

        self.assertIn("Claude 和 GPT 模型对比", prompt)
        self.assertIn("抖音科技爱好者", prompt)
        self.assertIn("开头 3 秒钩子", prompt)
        self.assertIn("模型来自 OpenAI-compatible API", prompt)


if __name__ == "__main__":
    unittest.main()
