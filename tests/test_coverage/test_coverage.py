import os
import re
import io
from unittest import TestCase, mock

from algo_profiler.coverage_check import CoverageLabels, CoverageCheck

from .functions import get_floor
from textwrap import dedent


class TestCoverageCheck(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.incomplete_test_set = [{"input": {"number": 1}, "output": 1}]
        cls.complete_test_set = [
            {"input": {"number": 1}, "output": 1},
            {"input": {"number": 1.0}, "output": 1},
        ]

    def test_removing_the_right_file(self):
        coverage = CoverageCheck(func=get_floor, test_set=self.incomplete_test_set)
        temp_file_path = ""

        with mock.patch("os.remove") as mock_remove:
            coverage.print_annotations()
            self.assertEqual(len(mock_remove.call_args_list), 1)
            temp_file_path = mock_remove.call_args.args[0]
            self.assertTrue(
                re.match("^.*/algo_profiler/temp_files/tests_test_coverage_functions.py,cover$", temp_file_path)
            )

        os.remove(temp_file_path)

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_fully_covered_data_set(self, mock_stdout):
        expected_result = f"\n{CoverageLabels.FULLY_COVERED}\n"
        coverage = CoverageCheck(func=get_floor, test_set=self.complete_test_set)
        coverage.test_coverage()
        self.assertEqual(mock_stdout.getvalue(), expected_result)

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_not_fully_covered_data_set(self, mock_stdout):
        expected_result = dedent(f"""\

        {CoverageLabels.MISSING_STMTS}

        {CoverageLabels.STMTS}          {CoverageLabels.MISSED_STMTS}              {CoverageLabels.COVER}               
        ------------------------------------------------------------
        7                   2                   71%                 
        ------------------------------------------------------------
          
        > from math import floor
          
        > def get_floor(number):
        >     if isinstance(number, int):
        >         return number
        !     else:
        !         return apply_floor(number)
        
        > def apply_floor(number):
        !     return floor(number)
          
        """)

        coverage = CoverageCheck(func=get_floor, test_set=self.incomplete_test_set)
        coverage.test_coverage()
        result = dedent(mock_stdout.getvalue())
        self.assertEqual(result, expected_result)
