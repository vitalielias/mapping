import hyperspy.api as hs
import os
import zipfile

class semReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata_list = []
        try:
            if self._is_zip_file():
                self._process_zip_file()
            else:
                self.metadata_list.append(self._extract_metadata(self.file_path))
        except Exception as e:
            print(f'Error loading metadata from {self.file_path}: {e}')

    def _is_zip_file(self):
        return zipfile.is_zipfile(self.file_path)

    def _process_zip_file(self):
        with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
            # Extract all files to a temporary directory
            temp_dir = "temp_metadata_files"
            zip_ref.extractall(temp_dir)
            
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                self.metadata_list.append(self._extract_metadata(file_path))
            
            # Cleanup the temporary directory after processing
            for file_name in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file_name))
            os.rmdir(temp_dir)

    def _extract_metadata(self, file_path):
        md = hs.load(file_path, lazy=True)
        return md.original_metadata.as_dictionary().get('CZ_SEM', {})

    def get_metadata(self):
        if not self.metadata_list:
            print("Metadata not loaded or empty.")
        return self.metadata_list

    def get_file_name(self):
        return os.path.splitext(os.path.basename(self.file_path))[0]
