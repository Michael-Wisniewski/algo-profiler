import io
import os
import pathlib
import sys
from textwrap import dedent
from unittest import TestCase, mock

from parameterized import parameterized

from src.tester import (StressTestResultFormatter, Tester,
                        TestLabels, TestResultFormatter)


class ResultFormatterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_set = [
            {"input": {"n": 1}, "output": 1},
            {"input": {"n": 1}, "output": 1, "label": "First expected label"},
            {"input": {"n": 1}, "output": 1},
            {"input": {"n": 1}, "output": 1, "label": "Second expected label"},
            {"input": {"n": 1}, "output": 1},
        ]

    def setUp(self):
        self.result_formatter = TestResultFormatter(self.test_set)

    @parameterized.expand(
        [
            (0, TestLabels.UNKNOWN),
            (1, "First expected label"),
            (2, TestLabels.UNKNOWN),
            (3, "Second expected label"),
            (4, TestLabels.UNKNOWN),
        ]
    )
    def test_format_text_test_label(self, test_idex, expected_label):
        test_label = self.result_formatter.format_test_label(test_idex)
        self.assertEqual(test_label, expected_label)

    @parameterized.expand(
        [
            (0, TestLabels.PASSED, f"1/5 {TestLabels.PASSED} {TestLabels.UNKNOWN}"),
            (1, TestLabels.FAILED, f"2/5 {TestLabels.FAILED} First expected label"),
            (2, TestLabels.CRASHED, f"3/5 {TestLabels.CRASHED} {TestLabels.UNKNOWN}"),
            (3, TestLabels.PASSED, f"4/5 {TestLabels.PASSED} Second expected label"),
            (4, TestLabels.FAILED, f"5/5 {TestLabels.FAILED} {TestLabels.UNKNOWN}"),
        ]
    )
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_display_counter_for_text_test_label(
        self, test_index, status_label, expected_counter, mock_stdout
    ):
        counter = self.result_formatter.display_counter(status_label=status_label, test_index=test_index)
        self.assertEqual(counter, expected_counter)
        self.assertEqual(counter + "\n", mock_stdout.getvalue())

    def test_format_assertion_error(self):
        expected_message = dedent(f"""\
        2/5 {TestLabels.FAILED} First expected label

        Lists differ: [1, 2] != [1, 2, 3]

        Second list contains 1 additional elements.
        First extra element 2:
        3

        - [1, 2]
        + [1, 2, 3]
        ?      +++

        """
        )

        with self.assertRaises(AssertionError) as context:
            self.assertEqual([1, 2], [1, 2, 3])

        formatted_error = self.result_formatter.format_assertion_error(test_index=1, exception=context.exception)
        self.assertEqual(formatted_error, expected_message)

    def test_format_uncaught_error(self):
        try:
            1 / 0
        except ZeroDivisionError as e:
            file_path = pathlib.Path(__file__).parent.absolute()
            file_name = os.path.basename(__file__)
            _, _, traceback = sys.exc_info()
            line_number = traceback.tb_lineno

            expected_message = dedent(f"""\
            3/5 {TestLabels.CRASHED} {TestLabels.UNKNOWN}

              File "{file_path}/{file_name}", line {line_number}, in test_format_uncaught_error
                1 / 0

            Error: division by zero
            """
            )

            formatted_error = self.result_formatter.format_uncaught_error(test_index=2, exception=e)
            self.assertEqual(formatted_error, expected_message)

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_append_passed_test(self, mock_stdout):
        expected_message = dedent(f"""\
        1/5 {TestLabels.PASSED} {TestLabels.UNKNOWN}
        
        {TestLabels.ALL_PASSED}

        """
        )

        self.result_formatter.append(0)
        self.result_formatter.display_errors()
        self.assertEqual(len(self.result_formatter.errors), 0)
        self.assertEqual(mock_stdout.getvalue(), expected_message)

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_append_tests_with_all_statuses(self, mock_stdout):
        file_path = pathlib.Path(__file__).parent.absolute()
        file_name = os.path.basename(__file__)
        uncaught_error_line = 0

        self.result_formatter.append(0)

        try:
            self.assertEqual([1, 2], [1, 2, 3])
        except AssertionError as e:
            self.result_formatter.append(1, e)

        try:
            1 / 0
        except ZeroDivisionError as e:
            _, _, traceback = sys.exc_info()
            uncaught_error_line = traceback.tb_lineno
            self.result_formatter.append(2, e)

        expected_message = dedent(f"""\
        1/5 {TestLabels.PASSED} {TestLabels.UNKNOWN}
        2/5 {TestLabels.FAILED} First expected label
        3/5 {TestLabels.CRASHED} {TestLabels.UNKNOWN}
        
        {TestLabels.SUMMARY}

        2/5 {TestLabels.FAILED} First expected label

        Lists differ: [1, 2] != [1, 2, 3]

        Second list contains 1 additional elements.
        First extra element 2:
        3

        - [1, 2]
        + [1, 2, 3]
        ?      +++


        3/5 {TestLabels.CRASHED} {TestLabels.UNKNOWN}

          File "{file_path}/{file_name}", line {uncaught_error_line}, in test_append_tests_with_all_statuses
            1 / 0

        Error: division by zero

        """
        )

        self.result_formatter.display_errors()
        self.assertEqual(len(self.result_formatter.errors), 2)
        self.assertEqual(mock_stdout.getvalue(), expected_message)


class StressTestsFormatterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        test_args = [1, 2, 3, 4, 5]
        cls.result_formatter = StressTestResultFormatter(test_args)

    @parameterized.expand(
        [
            (0, "Datagen argument: 1"),
            (1, "Datagen argument: 2"),
            (2, "Datagen argument: 3"),
            (3, "Datagen argument: 4"),
            (4, "Datagen argument: 5"),
        ]
    )
    def test_format_integer_test_label(self, test_idex, expected_label):
        test_label = self.result_formatter.format_test_label(test_idex)
        self.assertEqual(test_label, expected_label)


class TestTester(TestCase):
    def setUp(self):
        self.tester = Tester()

    @property
    def test_func(self):
        return lambda n: n / n if n <= 10 else n

    @property
    def test_naive_func(self):
        return lambda n: 1

    @property
    def test_data_gen(self):
        return lambda n: {"n": n}

    @parameterized.expand(
        [
            (
                "when success",
                [{"input": {"n": 1}, "output": 1}],
                TestLabels.PASSED),
            (
                "when assertion failed",
                [{"input": {"n": 1}, "output": 2}],
                TestLabels.FAILED,
            ),
            (
                "when function crashed",
                [{"input": {"n": 0}, "output": 1}],
                TestLabels.CRASHED,
            ),
        ]
    )
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_unit_test_run_status(self, _, test_set, test_status_label, mock_stdout):
        expected_message = f"1/1 {test_status_label} {TestLabels.UNKNOWN}\n\n"
        self.tester.run_unit_tests(func=self.test_func, test_set=test_set)
        self.assertTrue(mock_stdout.getvalue().startswith(expected_message))

    @parameterized.expand(
        [
            ("when success", 1, TestLabels.PASSED),
            ("when assertion failed", 100, TestLabels.FAILED),
            ("when function crashed", 0, TestLabels.CRASHED),
        ]
    )
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_stress_test_run_status(self, _, wanted_arg, test_status_label, mock_stdout):
        expected_message = f"1/1 {test_status_label} Datagen argument: {wanted_arg}"
        self.tester.run_stress_tests(
            func=self.test_func,
            naive_func=self.test_naive_func,
            data_gen=self.test_data_gen,
            gen_min_arg=wanted_arg,
            gen_max_arg=wanted_arg,
            gen_steps=1,
        )
        self.assertTrue(mock_stdout.getvalue().startswith(expected_message))
