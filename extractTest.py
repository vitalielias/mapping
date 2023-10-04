from semExtractor import MetadataExtractor

# Path to the known TIFF image that works for all three extraction methods
known_tiff_path = "/path/to/known/tiff/image.tif"

def test_metadata_extraction_methods(tiff_path):
    extractor = MetadataExtractor(tiff_path)
    
    methods = {
        "Hyperspy": extractor.hyperspy_extract,
        "PIL": extractor.pil_extract,
        "Zeiss": extractor.zeiss_extract
    }

    metadata_lengths = {}

    # Extract metadata using each method and store the length of the metadata
    for method_name, method in methods.items():
        metadata = method()
        if not metadata.get("error"):
            metadata_lengths[method_name] = len(metadata)
        else:
            print(f"Error encountered with {method_name} method.")
            metadata_lengths[method_name] = 0

    # Check if all methods produced the same length of metadata
    if len(set(metadata_lengths.values())) == 1:
        print("All methods produced the same length of metadata.")
    else:
        for method_name, length in metadata_lengths.items():
            print(f"{method_name} method produced metadata of length: {length}")

test_metadata_extraction_methods(known_tiff_path)
