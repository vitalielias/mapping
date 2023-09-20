import json
import os
import zipfile

class JsonOutputter:
    def __init__(self, mapped_metadata):
        self.mapped_metadata = mapped_metadata

    def _create_nested_structure(self, keys, value, dictionary):
        if len(keys) == 1:
            dictionary[keys[0]] = value
        else:
            key = keys.pop(0)
            if key not in dictionary:
                dictionary[key] = {}
            self._create_nested_structure(keys, value, dictionary[key])

    def generate_nested_json(self):
        nested_dict = {}
        for key, value in self.mapped_metadata.items():
            keys_list = key.split('.')
            self._create_nested_structure(keys_list, value, nested_dict)
        return nested_dict

    def save_to_file(self, file_path):
        nested_json = self.generate_nested_json()
        with open(file_path + 'output.json', 'w') as f:
            json.dump(nested_json, f, indent=4)
        print(f'File output to {file_path}.')
        return file_path  # Return the path of the saved file
    
    @staticmethod
    def save_to_zip(zip_filename, data_list, outputPath):
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for idx, data in enumerate(data_list):
                outputter = JsonOutputter(data)
                nested_json = outputter.generate_nested_json()
                json_content = json.dumps(nested_json, indent=4)
                output_file_name = f"{os.path.basename(zip_filename).replace('.zip', '')}_{idx}.json"
                zipf.writestr(output_file_name, json_content)


        # JsonOutputter.remove_hidden_files(outputPath)

    @staticmethod
    def remove_hidden_files(directory):
        for filename in os.listdir(directory):
            if filename.startswith('.'):
                try:
                    os.remove(os.path.join(directory, filename))
                except Exception as e:
                    print(f"Error deleting hidden file {filename}: {e}")



