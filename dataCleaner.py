from datetime import datetime

class DataCleaner:

    @staticmethod
    def clean_date_format(metadata):
        """
        Convert date and time from the metadata to ISO 8601 format.
        """
        date_str = metadata.get("entry.endTime.Date", "")
        time_str = metadata.get("entry.endTime.Time", "")
        
        # Convert to ISO 8601 format
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%d %b %Y %H:%M:%S")
            iso_format = dt.isoformat()
            metadata["entry.endTime"] = iso_format
        except ValueError:
            print(f"Error: Unable to convert date and time for {metadata.get('entry.title', '')}")

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
            "\u00b0": "degree"
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