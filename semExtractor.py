from PIL import Image
import hyperspy.api as hs
import tifffile

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
                return img.tag_v2
        except Exception as e:
            return {"error": str(e)}

    def zeiss_extract(self) -> dict:
        """
        Extracts metadata using the Zeiss TIFF reader method.

        Returns:
            dict: Extracted metadata as a Python dictionary.
        """
        try:
            # Assuming `tifffile` is the Zeiss TIFF reader
            with tifffile.TiffFile(self.file_path) as tif:
                return tif.pages[0].tags
        except Exception as e:
            return {"error": str(e)}

    def extract(self) -> dict:
        """
        Tries all metadata extraction methods and prints the outcome for each.

        Returns:
            dict: Extracted metadata from the first successful method or an error message if all methods fail.
        """
        methods = {
            "Hyperspy": self.hyperspy_extract,
            "PIL": self.pil_extract,
            "Zeiss": self.zeiss_extract
        }

        successful_metadata = None

        for method_name, method in methods.items():
            metadata = method()
            if not metadata.get("error"):
                print(f"Metadata extraction succeeded using {method_name} method.")
                if not successful_metadata:
                    successful_metadata = metadata
            else:
                print(f"Metadata extraction failed using {method_name} method.")

        if successful_metadata:
            return successful_metadata
        else:
            print("All extraction methods failed.")
            return {"error": "All extraction methods failed."}


