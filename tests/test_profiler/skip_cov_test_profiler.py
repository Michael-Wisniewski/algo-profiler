from unittest import TestCase, mock
from algo_profiler.profiler import Profiler
from .functions import increment_by_one

class TestProfiler(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profiler = Profiler()

    @property
    def test_set(self):
        return [
            {
                "label": "Empty list",
                "input": {
                    "numbers_list": [],
                },
                "output": [],
            },
            {
                "label": "List with positive numbers.",
                "input": {
                    "numbers_list": [1, 5, 7],
                },
                "output": [2, 6, 8],
            },
            {
                "label": "List with negative numbers.",
                "input": {
                    "numbers_list": [-2, -7, -3],
                },
                "output": [-1, -6, -2],
            },
            {
                "label": "List with large numbers.",
                "input": {
                    "numbers_list": [100000000, 9999999999999999999],
                },
                "output": [100000001, 10000000000000000000],
            },
        ]

    @property
    def data_gen(self):
        def func(list_length):
            """
            >>> data_gen(3)
            {'numbers_list': [0, 1, 2]}

            >>> data_gen(7)
            {'numbers_list': [0, 1, 2, 3, 4, 5, 6]}
            """

            numbers_list = [number for number in range(list_length)]
            return {"numbers_list" : numbers_list}

        return func

    @property
    def naive_increment_by_one(self):
        def func(numbers_list):
            return [number + 1 for number in numbers_list]

        return func

    def test_run_test(self):
        self.profiler.run_tests(func=increment_by_one, test_set=self.test_set)

    def test_run_stress_test(self):
        self.profiler.run_stress_tests(
            func=increment_by_one,
            naive_func=self.naive_increment_by_one,
            data_gen=self.data_gen,
            gen_min_arg=1,
            gen_max_arg=10,
            gen_steps=5,
            label="Test run",
        )

    def test_run_coverage(self):
        self.profiler.run_coverage(func=increment_by_one, test_set=self.test_set)

    def test_run_time_check(self):
        kwargs = self.data_gen(100)
        self.profiler.run_time_check(func=increment_by_one, kwargs=kwargs)

    def test_run_time_check_with_iterations(self):
        kwargs = self.data_gen(100)
        self.profiler.run_time_check(func=increment_by_one, kwargs=kwargs, iterations=10)

    def test_run_cProfile(self):
        kwargs = self.data_gen(100)
        self.profiler.run_cProfile(func=increment_by_one, kwargs=kwargs)

    @mock.patch("algo_profiler.profiler.run_snakeviz_server")
    def test_run_snakeviz(self, mock_snakeviz_server):
        kwargs = self.data_gen(100)
        self.profiler.run_snakeviz(func=increment_by_one, kwargs=kwargs)
        self.assertEqual(mock_snakeviz_server.call_count, 1)

    def test_run_line_profiler(self):
        kwargs = self.data_gen(100)
        self.profiler.run_line_profiler(func=increment_by_one, kwargs=kwargs)

    def test_run_time_analysis(self):
        self.profiler.run_time_analysis(
            func=increment_by_one,
            data_gen=self.data_gen,
            gen_min_arg=1,
            gen_max_arg=10,
            gen_steps=5,
        )

    def test_run_memory_check(self):
        kwargs = self.data_gen(100)
        self.profiler.run_memory_check(func=increment_by_one, kwargs=kwargs)

    def test_run_memory_profiler(self):
        kwargs = self.data_gen(100)
        self.profiler.run_memory_profiler(func=increment_by_one, kwargs=kwargs, clean_result=True)

    @mock.patch("algo_profiler.memory_check.plt")
    def test_run_time_based_memory_usage(self, mock_plt):
        kwargs = self.data_gen(100)
        self.profiler.run_time_based_memory_usage(func=increment_by_one, kwargs=kwargs, interval=0.01)
        self.assertEqual(mock_plt.show.call_count, 1)

    def test_run_check_memory_leaks(self):
        kwargs = self.data_gen(100)
        self.profiler.run_check_memory_leaks(func=increment_by_one, kwargs=kwargs, num_of_checks=1)

    def test_run_memory_analysis(self):
        self.profiler.run_memory_analysis(
            func=increment_by_one,
            data_gen=self.data_gen,
            gen_min_arg=1,
            gen_max_arg=10,
            gen_steps=5,
        )

    def test_run_scalene(self):
        kwargs = self.data_gen(100)
        self.profiler.run_scalene(func=increment_by_one, kwargs=kwargs)
