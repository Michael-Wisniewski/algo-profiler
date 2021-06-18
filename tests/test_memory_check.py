from sys import getsizeof
from unittest import TestCase

from src.memory_check import MemoryCheck


class TestMemoryCheck(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memory_check = MemoryCheck()

    @property
    def test_func(self):
        def create_list(n):
            return [1] * 10 ** 5 * n

        return create_list

    def test_get_memory_usage(self):
        kwargs_size_1, peak_usage_1, total_usage_1 = self.memory_check.get_mem_usage(self.test_func, kwargs={"n": 1})

        self.assertTrue(isinstance(kwargs_size_1, float))
        self.assertTrue(isinstance(peak_usage_1, float))
        self.assertTrue(isinstance(total_usage_1, float))

        self.assertTrue(kwargs_size_1 > 0)
        self.assertTrue(peak_usage_1 > 0)
        self.assertTrue(total_usage_1 > 0)

        kwargs_size_2, peak_usage_2, total_usage_2 = self.memory_check.get_mem_usage(self.test_func, kwargs={"n": 3})
        self.assertTrue(total_usage_2 > total_usage_1)

        self.assertTrue(kwargs_size_2 == kwargs_size_1)
        self.assertTrue(peak_usage_2 > peak_usage_1)
        self.assertTrue(total_usage_2 > total_usage_1)
