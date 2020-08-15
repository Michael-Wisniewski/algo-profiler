from unittest import TestCase

from parameterized import parameterized

from src.schema_check import DataErrorLabels, SchemaCheckMixin


class TestSchemaCheck(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema_checker = SchemaCheckMixin()

    @parameterized.expand(
        [
            (
                "test set is not a list",
                {"input": {"n": 1}, "output": 1},
                DataErrorLabels.NOT_A_LIST,
            ),
            (
                "test case is not a dict",
                [["input", 1, "output", 1]],
                DataErrorLabels.WRONG_SCHEMA,
            ),
            (
                "test case missing input key",
                [{"input": {"n": 1}, "output": 1}, {"output": 1}],
                DataErrorLabels.WRONG_SCHEMA,
            ),
            (
                "test case missing output key",
                [{"input": {"n": 1}, "output": 1}, {"input": {"n": 1}}],
                DataErrorLabels.WRONG_SCHEMA,
            ),
            (
                "empty test case",
                [{"input": {"n": 1}, "output": 1}, {}],
                DataErrorLabels.WRONG_SCHEMA,
            ),
            (
                "test case input is not a dict",
                [{"input": {"n": 1}, "output": 1}, {"input": 1, "output": 1}],
                DataErrorLabels.WRONG_SCHEMA,
            ),
            (
                "test case has wrong label type",
                [{"input": {"n": 1}, "output": 1, "label": 1}],
                DataErrorLabels.NOT_A_TEXT,
            ),
        ]
    )
    def test_schema_validation_raises_exception(self, _, test_set, exception_label):
        with self.assertRaises(TypeError) as context:
            self.schema_checker.validate_test_set_schema(test_set=test_set)

        self.assertEqual(str(context.exception), str(exception_label))
