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
        result_1 = self.memory_check.get_mem_usage(self.test_func, kwargs={"n": 1})

        self.assertTrue(isinstance(result_1, float))
        self.assertTrue(result_1 > 0)

        result_2 = self.memory_check.get_mem_usage(self.test_func, kwargs={"n": 3})
        self.assertTrue(result_2 > result_1)

        result_3 = self.memory_check.get_mem_usage(self.test_func, kwargs={"n": 5})
        self.assertTrue(result_3 > result_2)
