import re
from unittest import TestCase, mock

from src.scalene_analyzer import scalene_analyzer

from .functions import sleep_miliseconds


class TestScalene(TestCase):
    @mock.patch("src.scalene_analyzer.Scalene")
    def test_scalene_main_was_called(self, mock_scalene):
        scalene_analyzer(func=sleep_miliseconds, kwargs={"n": 1000})
        self.assertEqual(mock_scalene.main.call_count, 1)

    def test_removing_the_right_files(self):
        temp_files_paths = []

        with mock.patch("os.remove") as mock_remove:
            scalene_analyzer(func=sleep_miliseconds, kwargs={"n": 1000})
            temp_files_paths = mock_remove.call_args_list

        executable_file_path = temp_files_paths[0][0][0]
        kwargs_file_path = temp_files_paths[1][0][0]

        self.assertTrue(
            re.match("^.*/src/temp_files/scalene_temp.py$", executable_file_path)
        )
        self.assertTrue(
            re.match("^.*/src/temp_files/kwargs_temp.pickle$", kwargs_file_path)
        )
