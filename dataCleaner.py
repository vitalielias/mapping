from datetime import datetime
from dateutil import parser

class DataCleaner:

    @staticmethod
    def clean_date_format(metadata):
        """
        Convert date and time from the 'entry.endTime' metadata to ISO 8601 format using dateutil parser.
        """
        datetime_str = metadata.get("entry.endTime", "")

        try:
            dt = parser.parse(datetime_str)
            iso_format = dt.isoformat()
            metadata["entry.endTime"] = iso_format
        except ValueError as e:
            print(f"Error: Unable to convert 'entry.endTime' to ISO 8601 format for {metadata.get('entry.title', '')}. Error: {e}")

        # Remove the old Date and Time keys
        metadata.pop("entry.endTime.Date", None)
        metadata.pop("entry.endTime.Time", None)
        
        return metadata
    
    @staticmethod
    def clean_pixel_count(metadata):
        """
        Split the pixel count string into xPixels and yPixels and store them as integers.
        """
        pixel_str = metadata.get("entry.instrument.imaging.numberOfPixels.xPixels", "")
        
        # Split the string into x and y dimensions
        try:
            x_pixels, y_pixels = map(int, pixel_str.split('*'))
            metadata["entry.instrument.imaging.numberOfPixels.xPixels"] = x_pixels
            metadata["entry.instrument.imaging.numberOfPixels.yPixels"] = y_pixels
        except ValueError:
            print(f"Error: Unable to split pixel count for {metadata.get('entry.title', '')}")

        return metadata

    @staticmethod
    def replace_special_characters(metadata):
        """
        Replace special Unicode characters with their corresponding strings.
        """
        # Define a mapping of Unicode escape sequences to replacement strings
        replacements = {
            "\u00b5": "µ",
            "\u00b0": "degrees"
        }

        # Recursively replace special characters in the metadata dictionary
        def recursive_replace(item):
            if isinstance(item, dict):
                for key, value in item.items():
                    item[key] = recursive_replace(value)
            elif isinstance(item, list):
                for idx, value in enumerate(item):
                    item[idx] = recursive_replace(value)
            elif isinstance(item, str):
                for unicode_char, replacement in replacements.items():
                    item = item.replace(unicode_char, replacement)
            return item

        metadata = recursive_replace(metadata)
        return metadata


