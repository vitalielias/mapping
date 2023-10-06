from semReader import SemReader
from semExtractor import MetadataExtractor
import os

# List of file paths to test
file_paths = [
    "/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/Au-Gr_06.tif",
    # "/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/csv_test_images.zip",
    # "/Users/elias/Downloads/230926_Vitali_ Korruptionspraevention _ Corruption Prevention_Zertifikat.pdf"
    "/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/FeMoOx_AntiA_04_1k5x_CN.tif",
    "/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/1-as-cast_16_Sch_10k_InLens.tif",
    "/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/SEM Image 2 - SliceImage - 001.tif",
    "/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/SEM_image_sample_FEI_Helios_Nanolab600.tif",
    "/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/SEM_image_sample_Thermo_Fisher_Helios_G4_PFIB_CXe.tif"
]

def test_reader_and_extractor(file_path):
    print(f"Testing file: {file_path}")
    
    reader = SemReader(file_path)
    
    # Determine file format
    file_format = reader.determine_file_format(file_path)
    print(f"Detected file format: {file_format}")

    # Initialize a variable to store the paths of the successfully read files
    read_file_paths = []

    # Test reading functions based on detected format
    if file_format == 'TIFF':
        try:
            tiff_path = reader.read_single_file(file_path)
            read_file_paths.append(tiff_path)
            print(f"Successfully read TIFF file: {tiff_path}")
        except ValueError as e:
            print(e)

    elif file_format == 'ZIP':
        try:
            extracted_files = reader.read_zip_file(file_path)
            read_file_paths.extend(extracted_files)
            print(f"Successfully extracted ZIP file. Found {len(extracted_files)} TIFF files.")
        except ValueError as e:
            print(e)

    else:
        print(f"Unsupported file format: {file_format}")

    # If the reading was successful, proceed to extract metadata for each file
    for read_file_path in read_file_paths:
        extractor = MetadataExtractor(read_file_path)
        metadata = extractor.extract()
        # Print a subset of the metadata (for brevity)
        subset_metadata = {k: metadata[k] for k in list(metadata)[:2]}
        print(f"Extracted Metadata (subset) for {read_file_path}: {subset_metadata}")

    print("-" * 50)  # Separator

for path in file_paths:
    test_reader_and_extractor(path)
