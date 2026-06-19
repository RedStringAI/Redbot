import subprocess
import sys
import unittest
from tempfile import TemporaryDirectory


class CliTests(unittest.TestCase):
    def test_cli_lists_templates(self):
        result = subprocess.run(
            [sys.executable, "-m", "redbot", "templates"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("research-brief", result.stdout)
        self.assertIn("short-video-script", result.stdout)

    def test_cli_demo_run_writes_artifact(self):
        with TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "redbot",
                    "run",
                    "weekly-report",
                    "--topic",
                    "本周 AI 项目推进",
                    "--audience",
                    "团队成员",
                    "--context",
                    "完成 Redbot MVP。",
                    "--demo",
                    "--workspace",
                    tmp,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Artifact", result.stdout)


if __name__ == "__main__":
    unittest.main()
