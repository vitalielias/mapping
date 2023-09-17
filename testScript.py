from semReader import semReader
from semMapper import semMapper
from jsonOutputter import JsonOutputter
import json
import os

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

if __name__ == "__main__":
    directory_path = '/Users/elias/Desktop/MatWerk_Projects/testImages'
    mapFile = '/Users/elias/Desktop/MatWerk_Projects/mapping/map_files/hsSemMap.json'
    outputPath = '/Users/elias/Desktop/MatWerk_Projects/mapping/results'
    
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.tif') or file_name.endswith('.zip'):
            file_path = os.path.join(directory_path, file_name)
            process_file(file_path, mapFile, outputPath)
