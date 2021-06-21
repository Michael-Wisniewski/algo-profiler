import io

from sys import getsizeof
from unittest import TestCase, mock

from src.memory_check import MemoryCheck, MemoryCheckResultFormatter
from src.big_o_analyzer import BigOLabels
from .functions import create_list, get_floor, test_data_gen

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
        self.memory_check.run_memory_profiler(func=get_floor, kwargs={"number": 1.0}, clean_result=True)
        result = mock_stdout.getvalue()
        self.assertIn("get_floor", result)
        self.assertIn("apply_floor", result)

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_run_memory_profiler_with_clean_output(self, mock_stdout):
        self.memory_check.run_memory_profiler(func=create_list, kwargs={"n": 1}, clean_result=True)
        result = mock_stdout.getvalue()
        self.assertIn("6   0.0000 MiB   0.0000 MiB", result)

    @mock.patch.object(MemoryCheckResultFormatter, "append")
    def test_run_memory_analysis(self, mock_append):
        self.memory_check.run_memory_analysis(
            func=create_list,
            data_gen=test_data_gen,
            gen_min_arg=6,
            gen_max_arg=7,
            gen_steps=2
        )
        self.assertTrue(len(mock_append.call_args_list) == 2)

        idnex_1, arg_1, kwargs_1, func_1, total_1 = mock_append.call_args_list[0][1].values()
        idnex_2, arg_2, kwargs_2, func_2, total_2 = mock_append.call_args_list[1][1].values()

        self.assertTrue(isinstance(idnex_1, int))
        self.assertTrue(isinstance(arg_1, int))
        self.assertTrue(isinstance(kwargs_1, float))
        self.assertTrue(isinstance(func_1, float))
        self.assertTrue(isinstance(total_1, float))

        self.assertEqual(idnex_1, 1)
        self.assertEqual(idnex_2, 2)
        self.assertEqual(arg_1, 6)
        self.assertEqual(arg_2, 7)
        self.assertEqual(kwargs_1, kwargs_1)
        self.assertTrue(func_2 > func_1)
        self.assertTrue(total_2 > total_1)

    @mock.patch("src.memory_check.plt")
    def test_run_memory_analysis_with_chart(self, mock_plt):
        self.memory_check.run_memory_analysis(
            func=create_list,
            data_gen=test_data_gen,
            gen_min_arg=6,
            gen_max_arg=7,
            gen_steps=2,
            draw_chart=True
        )

        mock_plt.title.assert_called_once_with("Memory usage")
        mock_plt.xlabel.assert_called_once_with("Data generator's argument")
        mock_plt.ylabel.assert_called_once_with("Memory [MB]")
        self.assertEqual(mock_plt.plot.call_count, 3)
        self.assertEqual(mock_plt.legend.call_count, 1)
        self.assertEqual(mock_plt.show.call_count, 1)

    @mock.patch("src.memory_check.plt")
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_run_memory_analysis_with_big_o(self, mock_stdout, mock_plt):
        self.memory_check.run_memory_analysis(
            func=create_list,
            data_gen=test_data_gen,
            gen_min_arg=5,
            gen_max_arg=7,
            gen_steps=3,
            find_big_o=True
        )

        mock_plt.title.assert_called_once_with("Memory usage")
        mock_plt.xlabel.assert_called_once_with("Data generator's argument")
        mock_plt.ylabel.assert_called_once_with("Memory [MB]")
        self.assertEqual(mock_plt.plot.call_count, 4)
        self.assertEqual(mock_plt.legend.call_count, 1)
        self.assertEqual(mock_plt.show.call_count, 1)

        self.assertIn(str(BigOLabels.RESULT), mock_stdout.getvalue())

