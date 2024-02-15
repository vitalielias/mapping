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

    def test_read_zip_file(self):
        # Arrange
        zip_file_path = "test_files/csv_test_images.zip"

        # Act
        reader = semReader(zip_file_path)
        result = reader._is_zip_file()  # Assuming _is_zip_file() checks for ZIP files

        # Assert
        self.assertTrue(result)  # Assert that the result is True for a ZIP file

    def test_read_tiff_file(self):
        # Arrange
        tiff_file_path = "test_files/1-as-cast_16_Sch_10k_InLens.tif"

        # Act
        reader = semReader(tiff_file_path)
        result = reader._is_zip_file()  # Assuming _is_zip_file() checks for ZIP files

        # Assert
        self.assertFalse(result)  # Assert that the result is False for a non-ZIP (TIFF) file

if __name__ == '__main__':
    unittest.main()
