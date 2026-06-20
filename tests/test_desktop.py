import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from redbot.desktop import DesktopLaunchConfig, launch_desktop


class DesktopTests(unittest.TestCase):
    def test_launch_desktop_writes_status_file_without_opening_browser(self):
        with TemporaryDirectory() as tmp:
            config = DesktopLaunchConfig(
                host="127.0.0.1",
                port=8799,
                workspace=Path(tmp),
                demo=True,
                open_browser=False,
                start_server=False,
            )

            status = launch_desktop(config)

            status_file = Path(tmp) / "desktop-status.json"
            saved = json.loads(status_file.read_text(encoding="utf-8"))
            self.assertEqual(status.local_url, "http://127.0.0.1:8799")
            self.assertEqual(saved["local_url"], "http://127.0.0.1:8799")
            self.assertEqual(saved["webhooks"]["feishu"], "http://127.0.0.1:8799/webhook/feishu")

    def test_launch_desktop_opens_browser_when_requested(self):
        with TemporaryDirectory() as tmp:
            config = DesktopLaunchConfig(
                host="127.0.0.1",
                port=8800,
                workspace=Path(tmp),
                demo=True,
                open_browser=True,
                start_server=False,
            )

            with patch("webbrowser.open") as browser_open:
                launch_desktop(config)

            browser_open.assert_called_once_with("http://127.0.0.1:8800")


if __name__ == "__main__":
    unittest.main()
