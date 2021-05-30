import traceback as tb
from unittest import TestCase

from .helpers import LabelBase
from .linear_space import linear_space
from .schema_check import SchemaCheckMixin


class TestLabels(LabelBase):
    PASSED = "PASSED"
    FAILED = "FAILED"
    CRASHED = "CRASHED"
    UNKNOWN = "UNKNOWN"
    ALL_PASSED = "ALL TESTS PASSED"
    SUMMARY = "FAILED TESTS SUMMARY"


class TestResultFormatter:
    def __init__(self, test_set):
        self.test_set = test_set
        self.errors = []

    def format_test_label(self, test_index):
        test_input = self.test_set[test_index]
        return test_input.get("label", TestLabels.UNKNOWN)

    def display_counter(self, status_label, test_index):
        counter = f"{test_index + 1}/{len(self.test_set)}"
        test_label = self.format_test_label(test_index)
        counter_text = f"{counter} {status_label} {test_label}"
        print(counter_text)
        return counter_text

    def format_assertion_error(self, test_index, exception):
        error_log = self.display_counter(TestLabels.FAILED, test_index)
        error_log += f"\n\n{str(exception)}\n"
        return error_log

    def format_uncaught_error(self, test_index, exception):
        traceback = tb.format_tb(exception.__traceback__, limit=-1)[0]
        error_log = self.display_counter(TestLabels.CRASHED, test_index)
        error_log += f"\n\n{traceback}\nError: {str(exception)}\n"
        return error_log

    def append(self, test_index, exception=None):
        if exception is None:
            self.display_counter(TestLabels.PASSED, test_index)
        elif isinstance(exception, AssertionError):
            error = self.format_assertion_error(test_index, exception)
            self.errors.append(error)
        else:
            error = self.format_uncaught_error(test_index, exception)
            self.errors.append(error)

    def display_errors(self):
        header = TestLabels.SUMMARY if self.errors else TestLabels.ALL_PASSED
        errors_log = "\n".join(self.errors)
        print(f"\n{header}\n\n{errors_log}")


class StressTestResultFormatter(TestResultFormatter):
    def format_test_label(self, test_index):
        test_input = self.test_set[test_index]
        return f"input: {test_input}"


class Tester(SchemaCheckMixin):
    def __init__(self):
        self.assertEqual = TestCase().assertEqual

    def run_unit_tests(self, func, test_set):
        self.validate_test_set_schema(test_set)
        results_formatter = TestResultFormatter(test_set)

        for test_index, test_data in enumerate(test_set):
            try:
                result = func(**test_data["input"])
                self.assertEqual(result, test_data["output"])
                results_formatter.append(test_index)
            except Exception as e:
                results_formatter.append(test_index, e)

        results_formatter.display_errors()

    def run_stress_tests(
        self, func, naive_func, data_gen, gen_min_arg, gen_max_arg, gen_steps
    ):
        test_args = linear_space(
            min_val=gen_min_arg, max_val=gen_max_arg, steps_num=gen_steps
        )
        results_formatter = StressTestResultFormatter(test_args)

        for test_index, test_arg in enumerate(test_args):
            test_data = data_gen(test_arg)

            try:
                result = func(**test_data)
                reference_result = naive_func(**test_data)
                self.assertEqual(result, reference_result)
                results_formatter.append(test_index)
            except Exception as e:
                results_formatter.append(test_index, e)

        results_formatter.display_errors()
