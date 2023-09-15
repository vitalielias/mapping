import json

class semMapper:
    def __init__(self, metadata, map_file_path):
        self.metadata = metadata
        with open(map_file_path, 'r') as f:
            self.mapping = json.load(f)
        self.mapped_metadata = {}

    def _map_metadata(self):
        for hyperspy_key, schema_info in self.mapping.items():
            if hyperspy_key in self.metadata:
                for key_type, schema_key in schema_info.items():
                    if key_type == "value":
                        index = 1
                    elif key_type == "unit":
                        index = 2
                    else:
                        continue

                    try:
                        value = self.metadata[hyperspy_key][index]
                        self.mapped_metadata[schema_key] = value
                    except (TypeError, IndexError):
                        print(f"Error processing {hyperspy_key} for {key_type}")

    def get_mapped_metadata(self):
        if not self.metadata:
            return {"message": "No metadata matching the schema is available. The file may be from an instrument that is too old to embed the required metadata, or a metadata file type which is incompatible with Hyperspy."}
        else:
            self._map_metadata()
        return self.mapped_metadata
