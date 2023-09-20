from datetime import datetime

class DataCleaner:

    @staticmethod
    def clean_date_format(metadata):
        """
        Convert date and time from the metadata to ISO 8601 format.
        """
        date_str = metadata.get("entry", {}).get("endTime", {}).get("Date", "")
        time_str = metadata.get("entry", {}).get("endTime", {}).get("Time", "")
        
        # Convert to ISO 8601 format
        try:
            dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%d %b %Y %H:%M:%S")
            iso_format = dt.isoformat()
            metadata["entry"]["endTime"] = iso_format
        except ValueError:
            print(f"Error: Unable to convert date and time for {metadata.get('entry', {}).get('title', '')}")

        # Remove the old Date and Time keys
        if "endTime" in metadata.get("entry", {}):
            metadata["entry"]["endTime"].pop("Date", None)
            metadata["entry"]["endTime"].pop("Time", None)
        return metadata
