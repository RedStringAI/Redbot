import json
import unittest
from unittest.mock import Mock, patch

from redbot.llm import LLMConfig, OpenAICompatibleClient


class LLMTests(unittest.TestCase):
    def test_llm_config_reads_openai_compatible_environment(self):
        with patch.dict(
            "os.environ",
            {
                "REDBOT_API_KEY": "sk-test",
                "REDBOT_BASE_URL": "https://gateway.example.com/v1",
                "REDBOT_MODEL": "claude-sonnet-4",
            },
        ):
            config = LLMConfig.from_env()

        self.assertEqual(config.api_key, "sk-test")
        self.assertEqual(config.base_url, "https://gateway.example.com/v1")
        self.assertEqual(config.model, "claude-sonnet-4")

    def test_openai_client_requires_api_key_for_real_requests(self):
        config = LLMConfig(api_key="", base_url="https://gateway.example.com/v1", model="gpt-4o")

        with self.assertRaisesRegex(ValueError, "REDBOT_API_KEY"):
            OpenAICompatibleClient(config)

    def test_openai_client_posts_chat_completion(self):
        config = LLMConfig(
            api_key="sk-test",
            base_url="https://gateway.example.com/v1",
            model="gpt-4o-mini",
        )
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read.return_value = json.dumps(
            {"choices": [{"message": {"content": "hello from model"}}]}
        ).encode("utf-8")

        with patch("urllib.request.urlopen", return_value=response) as urlopen:
            client = OpenAICompatibleClient(config)
            result = client._complete_sync("Say hello")

        self.assertEqual(result, "hello from model")
        request = urlopen.call_args.args[0]
        self.assertEqual(request.headers["Authorization"], "Bearer sk-test")
        self.assertIn(b'"model": "gpt-4o-mini"', request.data)


if __name__ == "__main__":
    unittest.main()
