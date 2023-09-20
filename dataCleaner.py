from datetime import datetime

class DataCleaner:

    @staticmethod
    def clean_date_format(metadata):
        """
        Convert date and time from the metadata to ISO 8601 format.
        """
        try:
            # Extract date and time from metadata
            date_str = metadata.get("entry", {}).get("endTime", {}).get("Date", "")
            time_str = metadata.get("entry", {}).get("endTime", {}).get("Time", "")
            
            # Convert to ISO 8601 format
            combined_str = f"{date_str} {time_str}"
            dt = datetime.strptime(combined_str, '%d %b %Y %H:%M:%S')
            iso_format = dt.isoformat()

            # Update metadata with the new format
            metadata["entry"]["endTime"] = iso_format

        except ValueError:
            print(f"Error: Unable to convert date and time for {metadata.get('entry', {}).get('title', '')}")

        return metadata
