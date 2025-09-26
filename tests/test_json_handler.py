import unittest
from unittest.mock import mock_open, patch

from repo_agent.chat_with_repo.json_handler import (
    JsonFileProcessor,
)


class TestJsonFileProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = JsonFileProcessor("test.json")

    @patch("builtins.open", new_callable=mock_open, read_data='{"file.py": [{"md_content": ["content1"]}]}')
    def test_read_json_file(self, mock_file):
        # Test read_json_file method
        data = self.processor.read_json_file()
        self.assertEqual(data, {"file.py": [{"md_content": ["content1"]}]})
        mock_file.assert_called_with("test.json", "r", encoding="utf-8")

    @patch.object(JsonFileProcessor, 'read_json_file')
    def test_extract_data(self, mock_read_json):
        # Test extract_data method
        mock_read_json.return_value = {"file.py": [{"md_content": ["content1"], "name": "func1", "code_content": "def func1(): pass"}]}
        md_contents, extracted_contents = self.processor.extract_data()
        self.assertIn("content1", md_contents)
        self.assertEqual(len(extracted_contents), 1)
        self.assertEqual(extracted_contents[0]["name"], "func1")

    @patch("builtins.open", new_callable=mock_open, read_data='{"file1.py": [{"name": "func1", "code_content": "def func1(): pass", "md_content": ["doc for func1"]}]}')
    def test_search_code_contents_by_name(self, mock_file):
        # Test search_code_contents_by_name method
        code_results, md_results = self.processor.search_code_contents_by_name("test.json", "func1")
        self.assertEqual(code_results, ["def func1(): pass"])
        self.assertEqual(md_results, [["doc for func1"]])
        mock_file.assert_called_with("test.json", "r", encoding="utf-8")


if __name__ == '__main__':
    unittest.main()