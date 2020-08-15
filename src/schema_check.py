from .helpers import LabelBase


class DataErrorLabels(LabelBase):
    NOT_A_LIST = "Test set should be a list of test cases."
    NOT_A_TEXT = "Test case label must be a text."
    WRONG_SCHEMA = """Test set must have the structure:
            [
                {
                    "label": (Optional - text field),
                    "input": ... ,
                    "output": ... ,
                },
            ]            
        """


class SchemaCheckMixin:
    def validate_test_case_schema(self, test_data):
        required_keys = set(("input", "output"))
        if (
            not isinstance(test_data, dict)
            or required_keys - test_data.keys()
            or not isinstance(test_data["input"], dict)
        ):
            raise TypeError(DataErrorLabels.WRONG_SCHEMA)

        if "label" in test_data and not isinstance(test_data["label"], str):
            raise TypeError(DataErrorLabels.NOT_A_TEXT)

    def validate_test_set_schema(self, test_set):
        if not isinstance(test_set, list):
            raise TypeError(DataErrorLabels.NOT_A_LIST)

        for test_data in test_set:
            self.validate_test_case_schema(test_data)
