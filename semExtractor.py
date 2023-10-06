from PIL import Image
import hyperspy.api as hs
import zeisstiffmeta as ztm

class MetadataExtractor:
    """
    Class for extracting metadata from TIFF files using multiple methods.

    Attributes:
        file_path (str): Path to the file from which metadata needs to be extracted.
    """
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
            return md.original_metadata.as_dictionary().get('CZ_SEM', {})
        except Exception as e:
            return {"error": str(e)}

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

        except Exception as e:
            return {"error": str(e)}

    def zeiss_extract(self) -> dict:
        """
        Extracts metadata using the Zeiss TIFF metadata reader.
        
        Returns:
            dict: Extracted metadata as a Python dictionary.
        """
        try:
            metadata_list = ztm.zeiss_meta(self.file_path)
            metadata = ztm.meta_to_dict_all(metadata_list)
            return metadata
        except Exception as e:
            return {"error": str(e)}

    def extract(self) -> dict:
        """
        Tries all metadata extraction methods and prints the outcome for each.

        Returns:
            dict: Feedback on the consistency of metadata lengths across methods or an error message if all methods fail.
        """
        methods = {
            "Hyperspy": self.hyperspy_extract,
            "PIL": self.pil_extract,
            "Zeiss": self.zeiss_extract
        }

        metadata_lengths = {}
        successful_methods = []

        for method_name, method in methods.items():
            metadata = method()
            if not metadata.get("error"):
                print(f"Metadata extraction succeeded using {method_name} method.")
                metadata_lengths[method_name] = len(metadata)
                successful_methods.append(method_name)
            else:
                print(f"Metadata extraction failed using {method_name} method.")

        if len(set(metadata_lengths.values())) == 1:
            return {"message": "All successful methods produced metadata of the same length."}
        else:
            return {"message": "Metadata lengths vary across methods.", "lengths": metadata_lengths}



