from unittest import TestCase, mock
from .functions import get_floor
from algo_profiler.profiling_by_line import run_profiling_by_line
import io


class TestLineProfiler(TestCase):

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_all_module_functions_were_profiled(self, mock_stdout):
        kwargs = {"number": 1}
        run_profiling_by_line(func=get_floor, kwargs=kwargs)
        self.assertIn("def get_floor(number):", mock_stdout.getvalue())
        self.assertIn("def apply_floor(number):", mock_stdout.getvalue())
