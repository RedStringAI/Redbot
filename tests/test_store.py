import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from redbot.store import RedbotStore


class StoreTests(unittest.TestCase):
    def test_memory_is_persisted_by_scope(self):
        with TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "redbot.db"
            store = RedbotStore(db_path)

            store.save_memory(scope="feishu:chat-1:user-1", key="tone", value="说话简洁一点")
            reopened = RedbotStore(db_path)

            self.assertEqual(reopened.get_memory("feishu:chat-1:user-1", "tone"), "说话简洁一点")
            self.assertEqual(reopened.list_memories("feishu:chat-1:user-1")["tone"], "说话简洁一点")

    def test_knowledge_documents_are_chunked_and_searchable(self):
        with TemporaryDirectory() as tmp:
            store = RedbotStore(Path(tmp) / "redbot.db")

            doc_id = store.add_document(
                title="Redbot 飞书部署说明",
                content="飞书群入口需要配置事件订阅 URL，Redbot 会把消息转成统一任务请求。",
                source="manual",
            )
            hits = store.search_knowledge("飞书 事件订阅", limit=3)

            self.assertGreater(doc_id, 0)
            self.assertEqual(hits[0].title, "Redbot 飞书部署说明")
            self.assertIn("事件订阅", hits[0].content)

    def test_recent_messages_are_returned_oldest_to_newest(self):
        with TemporaryDirectory() as tmp:
            store = RedbotStore(Path(tmp) / "redbot.db")

            store.record_message("local", "room-1", "u1", "第一条", direction="in")
            store.record_message("local", "room-1", "redbot", "回复", direction="out")
            store.record_message("local", "room-1", "u1", "第二条", direction="in")

            recent = store.recent_messages("local", "room-1", limit=2)

            self.assertEqual([message.text for message in recent], ["回复", "第二条"])


if __name__ == "__main__":
    unittest.main()
