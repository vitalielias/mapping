import unittest
from unittest.mock import patch
from semMapper import semMapper

class TestSemMapper(unittest.TestCase):
    '''
    test_get_mapped_metadata_empty_mapping: Tests how semMapper handles an empty mapping file. It uses unittest.mock.patch to mock the json.load function, simulating an empty mapping file. The test verifies that the mapper returns a list containing a single dictionary with a "message" key, indicating no metadata could be mapped.
    test_get_mapped_metadata_valid_mapping: Tests the mapping functionality with a valid mock mapping. It mocks the json.load function to return a predefined mapping dictionary. The test then verifies that the semMapper correctly transforms the mock metadata according to this mapping.
    '''
    def setUp(self):
        # Mock metadata that simulates the output from semReader
        self.mock_metadata_list = [{
            'CZ_SEM.Signal1': ['Value1', 'unit1'],
            'CZ_SEM.Signal2': ['Value2', 'unit2'],
        }]

        # Mock mapping to simulate a simple mapping file
        self.mock_mapping = {
            'CZ_SEM.Signal1': {'value': 'Mapped.Signal1.Value', 'unit': 'Mapped.Signal1.Unit'},
            'CZ_SEM.Signal2': {'value': 'Mapped.Signal2.Value', 'unit': 'Mapped.Signal2.Unit'},
        }

    @patch('semMapper.json.load', return_value={})
    def test_get_mapped_metadata_empty_mapping(self, mock_json_load):
        mapper = semMapper(self.mock_metadata_list, 'fake_map_file.json')
        mapped_metadata_list = mapper.get_mapped_metadata()
        self.assertEqual(len(mapped_metadata_list), 1)
        self.assertIn('message', mapped_metadata_list[0])

    @patch('semMapper.json.load', return_value=mock_mapping)
    def test_get_mapped_metadata_valid_mapping(self, mock_json_load):
        mapper = semMapper(self.mock_metadata_list, 'fake_map_file.json')
        mapped_metadata_list = mapper.get_mapped_metadata()

        expected_mapped_metadata = [{
            'Mapped.Signal1.Value': 'Value1',
            'Mapped.Signal1.Unit': 'unit1',
            'Mapped.Signal2.Value': 'Value2',
            'Mapped.Signal2.Unit': 'unit2',
        }]

        self.assertEqual(mapped_metadata_list, expected_mapped_metadata)

if __name__ == '__main__':
    unittest.main()
