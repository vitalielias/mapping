import json
import os

def compare_files(test_files_dir, expected_files_dir):
    """
    Compares JSON files in the test_files_dir with their expected versions in expected_files_dir.

    Parameters:
    - test_files_dir: Directory containing the output JSON files from the tests.
    - expected_files_dir: Directory containing the expected JSON files.

    Returns:
    - A list of tuples, each containing the filename and a boolean indicating if the file matches the expected output.
    """
    comparison_results = []

    # List all JSON files in the test files directory
    test_files = [f for f in os.listdir(test_files_dir) if f.endswith('.json')]

    for test_file in test_files:
        test_file_path = os.path.join(test_files_dir, test_file)
        expected_file_path = os.path.join(expected_files_dir, test_file)

        # Check if the expected file exists
        if not os.path.exists(expected_file_path):
            print(f"Expected file does not exist: {expected_file_path}")
            comparison_results.append((test_file, False))
            continue

        # Load and compare the files
        with open(test_file_path, 'r') as tf, open(expected_file_path, 'r') as ef:
            test_data = json.load(tf)
            expected_data = json.load(ef)

            if test_data == expected_data:
                comparison_results.append((test_file, True))
            else:
                comparison_results.append((test_file, False))

    return comparison_results

def main():
    test_files_dir = 'test_files'
    expected_files_dir = 'test_files/TF_to_JSON/expected_results'
    results = compare_files(test_files_dir, expected_files_dir)

    all_match = True
    for filename, matches in results:
        if not matches:
            print(f"File does not match expected output: {filename}")
            all_match = False

    if all_match:
        print("All files match the expected output.")
    else:
        print("Some files do not match the expected output.")

if __name__ == "__main__":
    main()
