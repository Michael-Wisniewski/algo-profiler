import io
from src.big_o_analyzer import BigOLabels
from src.timer import TimerResultFormatter, TimerLabels, Timer
from unittest import TestCase, mock
from textwrap import dedent
import time


class TestTimerResultFormatter(TestCase):
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_append_rows(self, mock_stdout):
        expected_headers_row = dedent(f"""\
        {TimerLabels.RUN_NUMBER}             {TimerLabels.RUN_ARGUMENT}      {TimerLabels.RUN_TIME}         
        ---------------------------------------------------------------------
        """
        )
        expected_first_row = dedent(f"""\
        1/2                    10                     100                    
        ---------------------------------------------------------------------
        """
        )
        expected_second_row = dedent(f"""\
        2/2                    20                     200                    
        ---------------------------------------------------------------------

        """
        )

        expected_result = expected_headers_row
        result_formatter = TimerResultFormatter(runs_num=2, func_name="sleep")
        self.assertEqual(mock_stdout.getvalue(), expected_result)

        expected_result += expected_first_row
        result_formatter.append(1, 10, 100)
        self.assertEqual(mock_stdout.getvalue(), expected_result)

        expected_result += expected_second_row
        result_formatter.append(2, 20, 200)
        self.assertEqual(mock_stdout.getvalue(), expected_result)


class TestTimer(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.timer = Timer()

    @property
    def sleep(self):
        return lambda n: time.sleep(n * 0.01)

    @property
    def test_data_gen(self):
        return lambda n: {"n": n}

    def test_get_tun_time(self):
        result_1 = self.timer.get_run_time(
            func=self.sleep, kwargs={"n": 1}, iterations=2
        )
        self.assertTrue(isinstance(result_1, float))
        self.assertTrue(result_1 > 0)

        result_2 = self.timer.get_run_time(
            func=self.sleep, kwargs={"n": 2}, iterations=2
        )
        self.assertTrue(result_2 > result_1)

        result_3 = self.timer.get_run_time(
            func=self.sleep, kwargs={"n": 3}, iterations=2
        )
        self.assertTrue(result_3 > result_2)

    @mock.patch.object(TimerResultFormatter, "append")
    def test_run_time_analysis(self, mock_append):
        self.timer.run_time_analysis(
            func=self.sleep,
            data_gen=self.test_data_gen,
            gen_min_arg=1,
            gen_max_arg=2,
            gen_steps=2
        )
        self.assertTrue(len(mock_append.call_args_list) == 2)

        run_idnex_1, run_arg_1, run_time_1 = mock_append.call_args_list[0][1].values()
        run_idnex_2, run_arg_2, run_time_2 = mock_append.call_args_list[1][1].values()

        self.assertTrue(isinstance(run_idnex_1, int))
        self.assertTrue(isinstance(run_arg_1, int))
        self.assertTrue(isinstance(run_time_1, float))

        self.assertEqual(run_idnex_1, 1)
        self.assertEqual(run_idnex_2, 2)
        self.assertEqual(run_arg_1, 1)
        self.assertEqual(run_arg_2, 2)
        self.assertTrue(run_time_2 > run_time_1)

    @mock.patch("src.timer.plt")
    def test_run_time_analysis_with_chart(self, mock_plt):
        self.timer.run_time_analysis(
            func=self.sleep,
            data_gen=self.test_data_gen,
            gen_min_arg=1,
            gen_max_arg=2,
            gen_steps=2,
            draw_chart=True
        )

        mock_plt.title.assert_called_once_with("Function run times")
        mock_plt.xlabel.assert_called_once_with("Data generator's argument [N]")
        mock_plt.ylabel.assert_called_once_with("Time [s]")
        self.assertEqual(mock_plt.plot.call_count, 1)
        self.assertEqual(mock_plt.legend.call_count, 1)
        self.assertEqual(mock_plt.show.call_count, 1)

    @mock.patch("src.timer.plt")
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_run_time_analysis_with_big_o(self, mock_stdout, mock_plt):
        self.timer.run_time_analysis(
            func=self.sleep,
            data_gen=self.test_data_gen,
            gen_min_arg=1,
            gen_max_arg=3,
            gen_steps=3,
            find_big_o=True
        )

        mock_plt.title.assert_called_once_with("Function run times")
        mock_plt.xlabel.assert_called_once_with("Data generator's argument [N]")
        mock_plt.ylabel.assert_called_once_with("Time [s]")
        self.assertEqual(mock_plt.plot.call_count, 2)
        self.assertEqual(mock_plt.legend.call_count, 1)
        self.assertEqual(mock_plt.show.call_count, 1)

        self.assertIn(str(BigOLabels.RESULT), mock_stdout.getvalue())
