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
