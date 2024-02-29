import unittest
from unittest.mock import patch, mock_open
from jsonOutputter import JsonOutputter

class TestJsonOutputter(unittest.TestCase):
    def setUp(self):
        self.outputter = JsonOutputter(mapped_metadata={
            'entry.instrument.detector.resolution.xPixels': 1024,
            'entry.instrument.detector.resolution.yPixels': 768,
            'entry.sample.name': 'Test Sample'
        })

    def test_generate_nested_json(self):
        expected_nested_json = {
            'entry': {
                'instrument': {
                    'detector': {
                        'resolution': {
                            'xPixels': 1024,
                            'yPixels': 768
                        }
                    }
                },
                'sample': {
                    'name': 'Test Sample'
                }
            }
        }
        nested_json = self.outputter.generate_nested_json()
        self.assertEqual(nested_json, expected_nested_json)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_to_file(self, mock_file):
        file_path = 'test_output.json'
        self.outputter.save_to_file(file_path)
        mock_file.assert_called_once_with(file_path, 'w')
        mock_file().write.assert_called_once()

if __name__ == '__main__':
    unittest.main()
