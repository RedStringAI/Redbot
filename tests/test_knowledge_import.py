import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from redbot.knowledge import import_path
from redbot.store import RedbotStore


class KnowledgeImportTests(unittest.TestCase):
    def test_imports_text_and_markdown_files_from_directory(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "guide.md").write_text("# 飞书指南\n事件订阅 URL 配置。", encoding="utf-8")
            (root / "notes.txt").write_text("企业微信机器人 webhook 配置。", encoding="utf-8")
            (root / "ignore.bin").write_bytes(b"\x00\x01")
            store = RedbotStore(root / "redbot.db")

            imported = import_path(store, root)

            self.assertEqual(imported, 2)
            self.assertEqual(store.search_knowledge("飞书")[0].title, "guide.md")
            self.assertEqual(store.search_knowledge("企业微信")[0].title, "notes.txt")


if __name__ == "__main__":
    unittest.main()
