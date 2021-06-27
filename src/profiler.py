import cProfile

from pympler import tracker

from .coverage_check import CoverageCheck
from .memory_check import MemoryCheck
from .printers import PrinterMixin
from .profiling_by_line import run_profiling_by_line
from .scalene_analyzer import scalene_analyzer
from .snakeviz_cli import run_snakeviz_server
from .tester import Tester
from .timer import Timer


class Profiler(PrinterMixin):
    """This class combines all profiling packages and allows to run them  by calling the specific methods."""

    def __init__(self):
        super().__init__()
        self.timer = Timer()
        self.memory_check = MemoryCheck()

    def run_tests(self, func, test_set):
        """Runs unit tests.

        Args:
            func (function): Function to run.
            test_set (nested list): List of test cases.

        Returns:
            None: Displays information about the performed tests. 
        """
        self.print_title("UNIT TESTS")
        self.print_function(func)
        tester = Tester()
        tester.run_unit_tests(func=func, test_set=test_set)

    def run_stress_tests(
        self,
        func,
        naive_func,
        data_gen,
        gen_min_arg,
        gen_max_arg,
        gen_steps,
        label=None,
    ):
        """Runs stress tests against two provided functions.

        Args:
            func (function): Function to run.
            naive_func (function): Reference function.
            data_gen (function): Function generating test arguments.
            gen_min_arg (int): Minimal argument for a generator function.
            gen_max_arg (int): Maximum argument for a generator function .
            gen_steps (int): Number of steps to perform.
            label (str): Optional label to display.

        Returns:
            None: Displays information about the performed stress tests.
        """
        self.print_title("STRESS TESTS")
        if label:
            self.print_title(label)
        self.print_function(func)
        self.print_function(naive_func)
        tester = Tester()
        tester.run_stress_tests(
            func=func,
            naive_func=naive_func,
            data_gen=data_gen,
            gen_min_arg=gen_min_arg,
            gen_max_arg=gen_max_arg,
            gen_steps=gen_steps,
        )

    def run_coverage(self, func, test_set):
        """Checks test coverage.

        Args:
            func (function): Function to run.
            test_set (nested list): List of test cases.

        Returns:
            None: Displays information about function test coverage. 
        """
        self.print_title("COVERAGE TEST")
        self.print_function(func)
        coverage_checker = CoverageCheck(func=func, test_set=test_set)
        coverage_checker.test_coverage()

    def run_time_check(self, func, kwargs, iterations=1):
        """Checks function runtime.

        Args:
            func (function): Function to run.
            kwargs (nested dict): Arguments to run the function.
            iterations (int): Number of function runs. Average runtime is calculated.

        Returns:
            None: Displays information about function runtime. 
        """
        self.print_title("TIME CHECK")
        self.print_function(func)
        self.print_kwargs(kwargs)
        run_time = self.timer.get_run_time(func=func, kwargs=kwargs, iterations=1)

        if iterations == 1:
            print(f"Function runtime: {run_time} sec")
        else:
            print(f"Avg runtime from {iterations} iterations: {run_time} sec")

    def run_cProfile(self, func, kwargs):
        """Runs cProfile.

        Args:
            func (function): Function to run.
            kwargs (nested dict): Arguments to run the function.

        Returns:
            None: Displays information from cProfile. 
        """
        self.print_title("C PROFILER")
        self.print_function(func)
        self.print_kwargs(kwargs)
        cProfile.runctx("func(**kwargs)", globals(), locals(), sort="cumtime")

    def run_snakeviz(self, func, kwargs):
        """Runs Snakeviz server.

        Args:
            func (function): Function to run.
            kwargs (nested dict): Arguments to run the function.

        Returns:
            None: Runs Snakeviz server and opens a new web browser tab. 
        """
        self.print_title("SNAKEVIZ")
        self.print_function(func)
        self.print_kwargs(kwargs)
        run_snakeviz_server(func, kwargs)

    def run_line_profiler(self, func, kwargs):
        """Runs line profiler.

        Args:
            func (function): Function to run.
            kwargs (nested dict): Arguments to run the function.

        Returns:
            None: Displays information from line profiler. 
        """
        self.print_title("LINE PROFILER")
        self.print_function(func)
        self.print_kwargs(kwargs)
        run_profiling_by_line(func, kwargs)

    def run_time_analysis(
        self,
        func,
        data_gen,
        gen_min_arg,
        gen_max_arg,
        gen_steps,
        iterations=1,
        draw_chart=False,
        find_big_o=False,
    ):
        """Runs function runtime analysis.

        Args:
            func (function): Function to run.
            data_gen (function): Function generating test arguments.
            gen_min_arg (int): Minimal argument for a generator function.
            gen_max_arg (int): Maximum argument for a generator function .
            gen_steps (int): Number of steps to perform.
            iterations (int): Number of runs for each step. Average time is calculated.
            draw_chart (bool): Determines whether the results will be presented in a chart.
            find_big_o (bool): Determines whether BigO will be predicted.

        Returns:
            None: Displays information about function runtime analysis.
        """
        self.print_title("TIME ANALYSIS")
        self.print_function(func)
        self.timer.run_time_analysis(
            func=func,
            data_gen=data_gen,
            gen_min_arg=gen_min_arg,
            gen_max_arg=gen_max_arg,
            gen_steps=gen_steps,
            iterations=iterations,
            draw_chart=draw_chart,
            find_big_o=find_big_o,
        )

    def run_memory_check(self, func, kwargs):
        """Checks function memory usage.

        Args:
            func (function): Function to run.
            kwargs (nested dict): Arguments to run the function.

        Returns:
            None: Displays information about function memory usage. 
        """
        self.print_title("MEMORY CHECK")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        self.memory_check.run_memory_check(func=func, kwargs=kwargs)

    def run_memory_profiler(self, func, kwargs, clean_result=False):
        """Runs memory profiler.

        Args:
            func (function): Function to run.
            kwargs (nested dict): Arguments to run the function.
            clean_result (bool): Determines whether the function memory usage will be extracted from total memory consumption.

        Returns:
            None: Displays information from memory profiler. 
        """
        self.print_title("MEMORY PROFILER")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        self.memory_check.run_memory_profiler(
            func=func, kwargs=kwargs, clean_result=clean_result
        )

    def run_time_based_memory_usage(self, func, kwargs, interval=0.1):
        """Checks time based memory usage.

        Args:
            func (function): Function to run.
            kwargs (nested dict): Arguments to run the function.
            interval (float): Frequency of measurements.

        Returns:
            None: Displays information about function time based memory usage. 
        """
        self.print_title("TIME BASED MEMORY USAGE")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        self.memory_check.run_time_based_memory_usage(
            func=func, kwargs=kwargs, interval=interval
        )

    def run_check_memory_leaks(self, func, kwargs, num_of_checks=3):
        """Checks memory leaks.

        Args:
            func (function): Function to run.
            kwargs (nested dict): Arguments to run the function.
            num_of_checks (int): Number of checks after the end of the function.

        Returns:
            None: Displays information about objects left in memory. 
        """
        self.print_title("MEMORY LEAK CHECK")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        tr = tracker.SummaryTracker()
        func(**kwargs)

        for i in range(1, num_of_checks + 1):
            self.print_title(f"MEMORY CONTROL AT THE END OF THE FUNCTION #{i}")
            tr.print_diff()

        print()

    def run_memory_analysis(
        self,
        func,
        data_gen,
        gen_min_arg,
        gen_max_arg,
        gen_steps,
        draw_chart=False,
        find_big_o=False,
    ):
        """Runs function memory usage analysis.

        Args:
            func (function): Function to run.
            data_gen (function): Function generating test arguments.
            gen_min_arg (int): Minimal argument for a generator function.
            gen_max_arg (int): Maximum argument for a generator function .
            gen_steps (int): Number of steps to perform.
            draw_chart (bool): Determines whether the results will be presented in a chart.
            find_big_o (bool): Determines whether BigO will be predicted.

        Returns:
            None: Displays information about function memory usage analysis.
        """
        self.print_title("MEMORY ANALYSIS")
        self.print_function(func)
        self.memory_check.run_memory_analysis(
            func=func,
            data_gen=data_gen,
            gen_min_arg=gen_min_arg,
            gen_max_arg=gen_max_arg,
            gen_steps=gen_steps,
            draw_chart=draw_chart,
            find_big_o=find_big_o,
        )

    def run_scalene(self, func, kwargs, cpu_sampling_rate=0.1):
        """Runs Scalene.

        Args:
            func (function): Function to run.
            kwargs (nested dict): Arguments to run the function.
            cpu_sampling_rate (float): Frequency of measurements.

        Returns:
            None: Displays information from Scalene. 
        """
        self.print_title("SCALENE")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        scalene_analyzer(func=func, kwargs=kwargs, cpu_sampling_rate=cpu_sampling_rate)
