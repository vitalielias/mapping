import hyperspy.api as hs
from PIL import Image

class MetadataExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def hyperspy_extract(self) -> dict:
        """
        Extracts metadata using the Hyperspy method.

        Returns:
            dict: Extracted metadata as a Python dictionary.
        """
        try:
            md = hs.load(self.file_path, lazy=True)
            metadata = md.original_metadata.as_dictionary().get('CZ_SEM', {})
            
            # If 'CZ_SEM' metadata is not empty, print the tag used
            if metadata:
                print("Metadata extracted using the 'CZ_SEM' tag.")
                metadata.pop('', None)
            else:
                non_flat_metadata = md.original_metadata.as_dictionary().get('fei_metadata', {})
                metadata = flatten_metadata_dict(non_flat_metadata)
                
                # If 'fei_metadata' metadata is not empty, print the tag used
                if metadata:
                    print("Metadata extracted using the 'fei_metadata' tag.")
            
            # If both 'CZ_SEM' and 'fei_metadata' are empty, return an error message
            if not metadata:
                return {"error": "Hyperspy could not extract the necessary metadata."}
            
            return metadata
        except Exception as e:
            return {"error": str(e)}
        
    def flatten_metadata_dict(d):
        """
        Flattens a nested dictionary by removing the top-level keys.
        
        Args:
            d (dict): The input nested dictionary.
            
        Returns:
            dict: The flattened dictionary with top-level keys removed.
        """
        flattened = {}
        for k, v in d.items():
            if isinstance(v, dict):
                flattened.update(flatten_dict(v))
            else:
                flattened[k] = v
        return flattened



    def pil_extract(self) -> dict:
        """
        Extracts metadata using the PIL tags method.
        
        Returns:
            dict: Extracted metadata as a Python dictionary.
        """
        try:
            with Image.open(self.file_path) as img:
                metadata = {}
                for tag, value in img.tag_v2.items():
                    if tag in [34118, 34682]:
                        lines = value.split("\n")
                        for line in lines:
                            if "=" in line:
                                key, val = line.split("=", 1)
                                key = key.strip()
                                values = tuple(val.strip().split())
                                if len(values) == 1:
                                    values = values[0]
                                metadata[key] = values
                return metadata
        except Exception as e:
            return {"error": str(e)}

    def extract(self):
        """
        Tries all metadata extraction methods and prints the outcome for each.

        Returns:
            tuple: Feedback message, metadata lengths, and metadata dictionaries from each method.
        """
        methods = {
            "Hyperspy": self.hyperspy_extract,
            "PIL": self.pil_extract
        }

        metadata_results = {}
        metadata_lengths = {}

        for method_name, method in methods.items():
            metadata = method()
            metadata_results[method_name] = metadata
            if not metadata.get("error"):
                metadata_lengths[method_name] = len(metadata)
                print(f"Metadata extraction succeeded using {method_name} method.")
            else:
                print(f"Metadata extraction failed using {method_name} method.")

        feedback = "Metadata lengths are consistent." if len(set(metadata_lengths.values())) <= 1 else "Metadata lengths vary between methods."

        return feedback, metadata_lengths, metadata_results