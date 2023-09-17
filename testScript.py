from semReader import semReader
from semMapper import semMapper
from jsonOutputter import JsonOutputter
import json
import os
import shutil

def process_file(file_path, mapFile, outputPath):
    reader = semReader(file_path)
    metadata_list = reader.get_metadata()
    fileName = reader.get_file_name()
    
    mapper = semMapper(metadata_list, mapFile)
    mapped_metadata_list = mapper.get_mapped_metadata()

    for idx, mapped_metadata in enumerate(mapped_metadata_list):
        outputter = JsonOutputter(mapped_metadata)
        output_file_name = f"{fileName}_{idx}.json" if len(mapped_metadata_list) > 1 else f"{fileName}.json"
        outputter.save_to_file(os.path.join(outputPath, output_file_name))
    return reader

if __name__ == "__main__":
    # input_file_path = '/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/csv_test_images.zip'
    input_file_path = '/Users/elias/Desktop/MatWerk_Projects/SEMtestImages/Au-Gr_06.tif'
    mapFile = '/Users/elias/Desktop/MatWerk_Projects/mapping/map_files/hsSemMap.json'
    outputPath = '/Users/elias/Desktop/MatWerk_Projects/mapping/results'
    
    reader_instance = process_file(input_file_path, mapFile, outputPath)
    
    temp_dir = reader_instance.get_temp_dir_path()
    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Error deleting temporary directory: {e}")
