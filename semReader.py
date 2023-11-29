import hyperspy.api as hs
import os
import zipfile
import shutil

class semReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata_list = []
        self.current_file_name = os.path.splitext(os.path.basename(file_path))[0]  # Default to the provided file name
        self.temp_dir_path = os.path.abspath("temp_metadata_files")
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
            temp_dir = self.temp_dir_path
            zip_ref.extractall(temp_dir)
            
            for root, dirs, files in os.walk(temp_dir):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    self.current_file_name = os.path.splitext(os.path.basename(file_path))[0]
                    self.metadata_list.append(self._extract_metadata(file_path))
            
            # Cleanup the temporary directory after processing
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Error deleting temporary directory: {e}")

    def _extract_metadata(self, file_path):
        md = hs.load(file_path, lazy=True)
        md_dict = md.original_metadata.as_dictionary()
        if 'CZ_SEM' in md_dict:
            metadata = md_dict.get('CZ_SEM')
        elif 'fei_metadata' in md_dict:
            metadata = md_dict.get('fei_metadata')
        else:
            metadata = {}

        return metadata

    def get_metadata(self):
        if not self.metadata_list:
            print("Metadata not loaded or empty.")
        return self.metadata_list

    def get_file_name(self):
        return self.current_file_name
    
    def get_temp_dir_path(self):
        return self.temp_dir_path






