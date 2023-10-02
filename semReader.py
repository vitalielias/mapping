import os
import zipfile

class SemReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def determine_file_format(self, file_path: str) -> str:
        """
        Determines the format of the given file.

        Args:
            file_path (str): Path to the input file.

        Returns:
            str: The format of the file ('TIFF', 'ZIP', 'UNKNOWN').
        """
        if file_path.endswith('.tiff') or file_path.endswith('.tif'):
            return 'TIFF'
        elif zipfile.is_zipfile(file_path):
            return 'ZIP'
        else:
            return 'UNKNOWN'

    def read_single_file(self, file_path: str) -> str:
        """
        Reads a single TIFF file.

        Args:
            file_path (str): Path to the TIFF file.

        Returns:
            str: Path to the TIFF file.
        """
        if self.determine_file_format(file_path) == 'TIFF':
            return file_path
        else:
            raise ValueError(f"File {file_path} is not a TIFF file.")

    def read_zip_file(self, file_path: str) -> str:
        """
        Reads a ZIP file and extracts its contents to a temporary directory.

        Args:
            file_path (str): Path to the ZIP file.

        Returns:
            str: Path to the temporary directory where the ZIP file contents are extracted.
        """
        if self.determine_file_format(file_path) == 'ZIP':
            self.temp_dir = os.path.abspath("temp_extracted_files")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            return self.temp_dir
        else:
            raise ValueError(f"File {file_path} is not a ZIP file.")

        
    def delete_temp_dir(self):
        """
        Deletes the temporary directory if it exists.
        """
        if hasattr(self, 'temp_dir'):
            try:
                shutil.rmtree(self.temp_dir)
                print(f"Successfully deleted temporary directory: {self.temp_dir}")
            except Exception as e:
                print(f"Error deleting temporary directory: {e}")
