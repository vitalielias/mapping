import unittest
from unittest.mock import patch, MagicMock
import runScript

class TestRunScript(unittest.TestCase):
    '''
    * Mocks semReader, semMapper, and JsonOutputter classes to prevent actual file reading, metadata mapping, and file writing during the test.
    * Sets up mock return values for methods called within process_file to simulate their behavior.
    * Calls process_file with mock arguments and verifies that it behaves as expected, specifically that it calls the mocked classes' methods correctly and returns the expected result format.
    '''
    @patch('runScript.semReader')
    @patch('runScript.semMapper')
    @patch('runScript.JsonOutputter')
    def test_process_file(self, MockJsonOutputter, MockSemMapper, MockSemReader):
        # Setup mock return values
        mock_metadata_list = [{'dummy_key': 'dummy_value'}]
        MockSemReader.return_value.get_metadata.return_value = mock_metadata_list
        MockSemReader.return_value.get_file_name.return_value = 'test_file'
        MockSemReader.return_value.get_temp_dir_path.return_value = '/tmp/dummy_path'

        mock_mapped_metadata_list = [{'mapped_key': 'mapped_value'}]
        MockSemMapper.return_value.get_mapped_metadata.return_value = mock_mapped_metadata_list

        mock_output_file_path = '/path/to/output_file.json'
        MockJsonOutputter.return_value.save_to_file.return_value = mock_output_file_path

        # Execute the process_file function
        map_file = 'path/to/map_file.json'
        input_file_path = 'path/to/input_file.tif'
        output_path = 'path/to/output'
        result = runScript.process_file(input_file_path, map_file, output_path)

        # Verify the interactions and the result
        MockSemReader.assert_called_once_with(input_file_path)
        MockSemMapper.assert_called_once_with(mock_metadata_list, map_file)
        MockJsonOutputter.assert_called_once()
        MockJsonOutputter.return_value.save_to_file.assert_called_once_with(output_path)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        self.assertIn(mock_output_file_path, result[1])

if __name__ == '__main__':
    unittest.main()
