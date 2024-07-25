import json
from dataCleaner import DataCleaner

class semMapper:
    def __init__(self, metadata_list, map_file_path):
        self.metadata_list = metadata_list
        with open(map_file_path, 'r') as f:
            self.mapping = json.load(f)
        self.mapped_metadata_list = []

    def _map_metadata(self, metadata):
        mapped_metadata = {}

        for key, value_tuple in metadata.items():
            print(f"Processing key: {key}, value_tuple: {value_tuple}")
            if not isinstance(value_tuple, tuple) or len(value_tuple) < 2:
                print(f"Warning: Unexpected tuple format for key: {key}, tuple: {value_tuple}")
                continue

            base_key = value_tuple[0]  # Extract the base key name
            if not isinstance(base_key, str):
                print(f"Warning: Unexpected base_key type for key: {key}, base_key: {base_key}")
                continue

            value = value_tuple[1]
            unit = value_tuple[2] if len(value_tuple) == 3 else None  # Handle missing unit

            mapped_key_value = self.mapping["mappedTerms"].get(base_key + "_value")
            mapped_key_unit = self.mapping["mappedTerms"].get(base_key + "_unit")

            if mapped_key_value:
                mapped_metadata[mapped_key_value] = value
            if mapped_key_unit and unit is not None:  # Check if unit mapping exists and unit is provided
                mapped_metadata[mapped_key_unit] = unit

        print(f"Mapped metadata: {mapped_metadata}")
        return mapped_metadata







    def get_mapped_metadata(self):
        if not self.metadata_list:
            return [{"message": "No metadata matching the schema is available. The file may be from an instrument that is too old to embed the required metadata, or a metadata file type which is incompatible with Hyperspy."}]
        else:
            print('Entering the for loop through metadata_list...')
            for metadata in self.metadata_list:
                if not metadata:  # Check if the metadata is empty
                    self.mapped_metadata_list.append({"message": "No metadata matching the schema is available. The file may be from an instrument that is too old to embed the required metadata, or a metadata file type which is incompatible with Hyperspy."})
                else:
                    # print(metadata)
                    # print('else statement triggered')
                    # print(f'result of _map_metadata(metadata): {self._map_metadata(metadata)}')
                    self.mapped_metadata_list.append(self._map_metadata(metadata))

        cleaner = DataCleaner()
        for metadata in self.mapped_metadata_list:
            cleaner.clean_date_format(metadata)
            cleaner.clean_pixel_count(metadata)
            cleaner.replace_special_characters(metadata)

        return self.mapped_metadata_list

