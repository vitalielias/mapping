import hyperspy.api as hs
import os

class semReader:
    def __init__(self, file_path):
        self.file_path = file_path
        try:
            self.metadata  = self._extract_metadata()
        except Exception as e:
            print(f'Error loading metadata from {self.file_path}: {e}')

    def _extract_metadata(self):
        md = hs.load(self.file_path, lazy = True)
        return md.original_metadata.as_dictionary().get('CZ_SEM', {})
    
    def get_metadata(self):
        if not self.metadata:
            print("Metadata not loaded or empty.")
        return self.metadata
    
    def get_file_name(self):
        return os.path.splitext(os.path.basename(self.file_path))[0]