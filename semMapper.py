import json
from dataCleaner import DataCleaner

class semMapper:
    def __init__(self, metadata_list, map_file_path):
        self.metadata_list = metadata_list
        with open(map_file_path, 'r') as f:
            self.mapping = json.load(f)
        self.mapped_metadata_list = []

    # def _map_metadata(self, metadata):
    #     mapped_metadata = {}
    #     for hyperspy_key, schema_info in self.mapping.items():
    #         if hyperspy_key in metadata:
    #             for key_type, schema_key in schema_info.items():
    #                 if key_type == "value":
    #                     index = 1
    #                 elif key_type == "unit":
    #                     index = 2
    #                 else:
    #                     continue

    #                 try:
    #                     value = metadata[hyperspy_key][index]
    #                     mapped_metadata[schema_key] = value
    #                 except (TypeError, IndexError):
    #                     print(f"Error processing {hyperspy_key} for {key_type}")
    #     return mapped_metadata
    
    def _map_metadata(self, metadata):
        """
        Map metadata keys according to the Thermo Fisher mapping.
        Only include keys in the resulting dictionary if a corresponding mapping is found.
        :param metadata: Dictionary containing metadata with original keys.
        :return: Dictionary containing metadata with only the keys found in the mapping.
        """
        mapped_metadata = {}
        print(f'Metadata to be mapped:\n {metadata}')
        for key, value in metadata.items():
            # Find the new key in the mapping where the current key is the value
            new_key = next((k for k, v in self.mapping.items() if v == key), None)
            if new_key:
                mapped_metadata[new_key] = value

        print(f'Here is the mapped metadata:\n {mapped_metadata}')
        return mapped_metadata

    def get_mapped_metadata(self):
        if not self.metadata_list:
            return [{"message": "No metadata matching the schema is available. The file may be from an instrument that is too old to embed the required metadata, or a metadata file type which is incompatible with Hyperspy."}]
        else:
            for metadata in self.metadata_list:
                if not metadata:  # Check if the metadata is empty
                    self.mapped_metadata_list.append({"message": "No metadata matching the schema is available. The file may be from an instrument that is too old to embed the required metadata, or a metadata file type which is incompatible with Hyperspy."})
                else:
                    self.mapped_metadata_list.append(self._map_metadata(metadata))
        
        cleaner = DataCleaner()
        for metadata in self.mapped_metadata_list:
            cleaner.clean_date_format(metadata)
        #     cleaner.clean_pixel_count(metadata)
        #     cleaner.replace_special_characters(metadata)

        return self.mapped_metadata_list

