from jsonschema import Draft7Validator

class SchemaValidator:
    def __init__(self, schema):
        self.schema = schema
        self.is_valid = False
        self.error_messages = []

    def validate(self, json_data):
        """
        Validate a JSON document against the provided schema and store all errors.
        
        Parameters:
        - json_data (dict): The JSON document to validate. The json Python parser can parse JSON documents as Python dict objects.
        """
        validator = Draft7Validator(self.schema)
        errors = sorted(validator.iter_errors(json_data), key = lambda e: e.path)

        if not errors:
            self.is_valid = True
            self.error_messages = ["JSON document is valid against the schema."]
        else:
            self.is_valid = False
            for error in errors:
                path_to_error = '.'.join([str(p) for p in error.path])
                self.error_messages.append(f"At '{path_to_error}: {error.message}")

    def get_validation_status(self):
        """
        Returns the validation status and associated error messages.
        
        Returns:
        - bool: True if the document is valid, False otherwise.
        - list: A list of error messages indicating the validation issues.
        """
        return self.is_valid, self.error_messages