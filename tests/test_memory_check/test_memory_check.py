import io

from sys import getsizeof
from unittest import TestCase, mock

from src.memory_check import MemoryCheck
from .functions import create_list, get_floor

class TestMemoryCheck(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memory_check = MemoryCheck()

    def test_get_memory_usage(self):
        kwargs_size_1, peak_usage_1, total_usage_1 = self.memory_check.get_mem_usage(func=create_list, kwargs={"n": 1})

        self.assertTrue(isinstance(kwargs_size_1, float))
        self.assertTrue(isinstance(peak_usage_1, float))
        self.assertTrue(isinstance(total_usage_1, float))

        self.assertTrue(kwargs_size_1 > 0)
        self.assertTrue(peak_usage_1 > 0)
        self.assertTrue(total_usage_1 > 0)

        kwargs_size_2, peak_usage_2, total_usage_2 = self.memory_check.get_mem_usage(func=create_list, kwargs={"n": 3})
        self.assertTrue(total_usage_2 > total_usage_1)

        self.assertTrue(kwargs_size_2 == kwargs_size_1)
        self.assertTrue(peak_usage_2 > peak_usage_1)
        self.assertTrue(total_usage_2 > total_usage_1)

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_run_memory_check(self, mock_stdout):
        self.memory_check.run_memory_check(func=create_list, kwargs={"n": 1})
        result = mock_stdout.getvalue()
        self.assertIn("Kwargs size", result)
        self.assertIn("Function usage", result)
        self.assertIn("Total usage", result)

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_run_memory_profiler_for_all_functions(self, mock_stdout):
        self.memory_check.run_memory_profiler(func=get_floor, kwargs={"number": 1.0})
        result = mock_stdout.getvalue()
        self.assertIn("get_floor", result)
        self.assertIn("apply_floor", result)

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_run_memory_profiler_with_clean_output(self, mock_stdout):
        self.memory_check.run_memory_profiler(func=create_list, kwargs={"n": 1}, clean_result=True)
        result = mock_stdout.getvalue() 
        self.assertIn("3   0.0000 MiB   0.0000 MiB", result)
        
    def test_run_memory_profiler_with_clean_output(self):
        self.memory_check.run_time_based_memory_usage(func=create_list, kwargs={"n": 1})
      
        