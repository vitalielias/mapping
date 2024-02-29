import unittest
import os
import json
from runnerScript

class TestRunnerScript(unittest.TestCase):
    def setUp(self):
        # Set the base directory for test files and expected results
        self.test_files_dir = os.path.join("tests", "test_files", "Zeiss_to_JSON")
        self.expected_results_dir = os.path.join(self.test_files_dir, "expected_results")

    def test_image_extraction(self):
        # List all TIFF files in the test directory
        for filename in os.listdir(self.test_files_dir):
            if filename.endswith(".tif"):
                # Construct file paths
                test_file_path = os.path.join(self.test_files_dir, filename)
                expected_result_path = os.path.join(self.expected_results_dir, f"{os.path.splitext(filename)[0]}.json")

                # Run the extraction script and get the result
                result = run_extraction(test_file_path)
                
                # Load the expected result
                with open(expected_result_path, 'r') as file:
                    expected_result = json.load(file)
                
                # Compare the result with the expected result
                self.assertEqual(result, expected_result, f"Failed for {filename}")

if __name__ == '__main__':
    unittest.main()
