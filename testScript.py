from semReader import semReader
from semMapper import semMapper
from jsonOutputter import JsonOutputter
import json
import os

def process_tiff(file_path, mapFile, outputPath):
    reader = semReader(file_path)
    metadata = reader.get_metadata()
    fileName = reader.get_file_name()
    
    mapper = semMapper(metadata, mapFile)
    mapped_metadata = mapper.get_mapped_metadata()

    outputter = JsonOutputter(mapped_metadata)
    outputter.save_to_file(os.path.join(outputPath, fileName + '.json'))

if __name__ == "__main__":
    # directory_path = "/Users/elias/Desktop/MatWerk_Projects/testImages"
    directory_path = '/Users/elias/Desktop/MatWerk_Projects/metadata_SEM_LM_Alexey/SEM_20230207to20230222'
    mapFile = '/Users/elias/Desktop/MatWerk_Projects/mapping/map_files/hsSemMap.json'
    outputPath = '/Users/elias/Desktop/MatWerk_Projects/mapping/results'
    
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.tif'):
            file_path = os.path.join(directory_path, file_name)
            process_tiff(file_path, mapFile, outputPath)
