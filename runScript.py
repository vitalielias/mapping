from semReader import semReader
from semMapper import semMapper
from jsonOutputter import JsonOutputter
import os
import shutil
import sys

def process_file(file_path, mapFile, outputPath):
    reader = semReader(file_path)
    metadata_list = reader.get_metadata()

    fileName = reader.get_file_name()
    
    mapper = semMapper(metadata_list, mapFile)  # Use the cleaned metadata here
    mapped_metadata_list = mapper.get_mapped_metadata()
    print(f'Here is the mapped metadata which the runScript receives:\n {mapped_metadata_list}')


    generated_files = []  # List to store paths of generated JSON files

    for idx, mapped_metadata in enumerate(mapped_metadata_list):
        outputter = JsonOutputter(mapped_metadata)
        output_file_name = f"{fileName}_{idx}.json" if len(mapped_metadata_list) > 1 else f"{fileName}.json"
        saved_file_path = outputter.save_to_file(os.path.join(outputPath, output_file_name))
        generated_files.append(saved_file_path)

    return reader, generated_files, mapped_metadata_list


if __name__ == "__main__":
    # input_file_path = '/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/1-as-cast_17_Sch_10k_SESI.tif'
    input_file_path = '/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/SEM_image_sample_Thermo_Fisher_Helios_G4_PFIB_CXe.tif'
    # input_file_path = '/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/P10_ID01#4-PtPd_080.tif'
    mapFile = '/Users/elias/Desktop/MatWerk_Projects/Metadata-Schemas-for-Materials-Science/SEM/map_SEM_ThermoFisher.json'
    # mapFile = '/Users/elias/Desktop/hsSemMap.json'
    outputPath = '/Users/elias/Desktop/MatWerk_Projects/mapping/results'
    
    # mapFile         = sys.argv[1]
    # input_file_path = sys.argv[2]
    # outputPath      = sys.argv[3]
    
    reader_instance, generated_files, mapped_metadata_list = process_file(input_file_path, mapFile, outputPath)
    
    # If the input was a zip file and multiple JSON files were generated, zip them together
    if input_file_path.endswith('.zip') and len(generated_files) > 1:
        zip_filename = os.path.join(outputPath, os.path.basename(input_file_path).replace('.zip', '_metadata_documents.zip'))
        # zip_filename = outputPath # only for use with mapping service
        JsonOutputter.save_to_zip(zip_filename, mapped_metadata_list, outputPath)
    
    # Clean up the temporary directory used for unzipping
    temp_dir = reader_instance.get_temp_dir_path()
    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Error deleting temporary directory: {e}")
