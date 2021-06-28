import os
import re
import sys
from unittest import TestCase, mock

from algo_profiler.snakeviz_cli import run_snakeviz_server


class TestSnakeviz(TestCase):
    @property
    def create_list(self):
        return lambda n: [0] * n

    @mock.patch("algo_profiler.snakeviz_cli.snakeviz")
    @mock.patch.object(sys, "argv")
    def test_removing_the_right_file(self, sys_args, mock_snakeviz):
        temp_file_path = ""
        kwargs = {"n": 1000}

        with mock.patch("os.remove") as mock_remove:
            run_snakeviz_server(func=self.create_list, kwargs=kwargs)
            self.assertEqual(mock_snakeviz.call_count, 1)

            self.assertEqual(len(mock_remove.call_args_list), 1)
            temp_file_path = mock_remove.call_args.args[0]

            sys_args.append.assert_called_once_with(temp_file_path)
            self.assertTrue(
                re.match("^.*/algo_profiler/temp_files/snakeviz.prof$", temp_file_path)
            )

        os.remove(temp_file_path)
