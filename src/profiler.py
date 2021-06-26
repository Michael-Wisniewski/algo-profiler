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
    def __init__(self):
        super().__init__()
        self.timer = Timer()
        self.memory_check = MemoryCheck()

    def run_tests(self, func, test_set):
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
        self.print_title("COVERAGE TEST")
        self.print_function(func)
        coverage_checker = CoverageCheck(func=func, test_set=test_set)
        coverage_checker.test_coverage()

    def run_time_check(self, func, kwargs, iterations=1):
        self.print_title("TIME CHECK")
        self.print_function(func)
        self.print_kwargs(kwargs)
        run_time = self.timer.get_run_time(func=func, kwargs=kwargs, iterations=1)

        if iterations == 1:
            print(f"Function run time: {run_time} sec")
        else:
            print(f"Avg run time from {iterations} iterations: {run_time} sec")

    def run_cProfile(self, func, kwargs):
        self.print_title("C PROFILER")
        self.print_function(func)
        self.print_kwargs(kwargs)
        cProfile.runctx("func(**kwargs)", globals(), locals(), sort="cumtime")

    def run_snakeviz(self, func, kwargs):
        self.print_title("SNAKEVIZ")
        self.print_function(func)
        self.print_kwargs(kwargs)
        run_snakeviz_server(func, kwargs)

    def run_line_profiler(self, func, kwargs):
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
        self.print_title("MEMORY CHECK")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        self.memory_check.run_memory_check(func=func, kwargs=kwargs)

    def run_memory_profiler(self, func, kwargs, clean_result=False):
        self.print_title("MEMORY PROFILER")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        self.memory_check.run_memory_profiler(
            func=func, kwargs=kwargs, clean_result=clean_result
        )

    def run_time_based_memory_usage(self, func, kwargs, interval=0.1):
        self.print_title("TIME BASED MEMORY USAGE")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        self.memory_check.run_time_based_memory_usage(
            func=func, kwargs=kwargs, interval=interval
        )

    def run_check_memory_leaks(self, func, kwargs, num_of_checks=3):
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
        self.print_title("SCALENE")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        scalene_analyzer(func=func, kwargs=kwargs, cpu_sampling_rate=cpu_sampling_rate)
