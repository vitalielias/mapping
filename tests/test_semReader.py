import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from semReader import semReader
import unittest


class TestSemReader(unittest.TestCase):
    def test_get_metadata(self):
        # Arrange
        test_file_path = "test_files/1-as-cast_16_Sch_10k_InLens.tif" 
        reader = semReader(test_file_path)

        # Act
        metadata = reader.get_metadata()

        # Assert
        self.assertIsNotNone(metadata)  # Check that metadata is not None
        # what other things do we want to check?

if __name__ == '__main__':
    unittest.main()
