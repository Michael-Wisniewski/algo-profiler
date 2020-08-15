import cProfile
import inspect

# import numpy as np
from line_profiler import LineProfiler
from .coverage_check import CoverageCheck
from .memory_check import MemoryCheck
from .printers import PrinterMixin
from .tester import Tester
from .timer import Timer

# from big_o import big_o, infer_big_o_class
# from big_o.complexities import ALL_CLASSES


class Profiler(PrinterMixin):
    def __init__(self, timer_iterations=10):
        super().__init__()
        self.tester = Tester()
        self.timer = Timer()
        self.memory_check = MemoryCheck()

    def run_tests(self, func, test_set):
        self.print_title("UNIT TESTS")
        self.print_function(func)
        self.tester.run_unit_tests(func=func, test_set=test_set)

    def run_stress_tests(
        self, func, naive_func, data_gen, gen_min_arg, gen_max_arg, gen_steps
    ):
        self.print_title("STRESS TESTS")
        self.print_function(func)
        self.print_function(naive_func)
        self.tester.run_stress_tests(
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

    def run_time_check(self, func, kwargs):
        self.print_title("TIME CHECK")
        self.print_function(func)
        self.print_kwargs(kwargs)
        run_time = self.timer.get_run_time(func=func, kwargs=kwargs)
        print(f"Function run time: {round(run_time, 6)} sec")

    def run_timer(
        self, func, data_gen, gen_min_arg, gen_max_arg, gen_steps, iterations
    ):
        self.print_title("TIMER")
        self.print_function(func)
        self.timer.run_timer(
            func=func,
            data_gen=data_gen,
            gen_min_arg=gen_min_arg,
            gen_max_arg=gen_max_arg,
            gen_steps=gen_steps,
            iterations=iterations,
        )

    def run_c_profiler(self, func, kwargs):
        self.print_title("C PROFILER")
        self.print_function(func)
        self.print_kwargs(kwargs)
        cProfile.runctx("func(**kwargs)", globals(), locals(), sort="cumtime")

    def run_line_profiler(self, func, kwargs):
        self.print_title("LINE PROFILER")
        self.print_function(func)
        self.print_kwargs(kwargs)
        line_profiler = LineProfiler()
        functions = inspect.getmembers(inspect.getmodule(func), inspect.isfunction)
        function_instances = dict(functions).values()

        for function_instance in function_instances:
            if function_instance is not func:
                line_profiler.add_function(function_instance)

        line_profiler_wrapper = line_profiler(func)
        line_profiler_wrapper(**kwargs)
        line_profiler.print_stats()

    def run_memory_check(self, func, kwargs):
        self.print_title("MEMORY CHECK")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        mem_usage = self.memory_check.get_mem_usage(func, kwargs)
        print(f"Memory usage: {round(mem_usage, 2)} MiB")

    def run_memory_profiler(self, func, kwargs):
        self.print_title("MEMORY PROFILER")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        self.memory_check.run_memory_check(func=func, kwargs=kwargs)

    # def run_time_big_o(
    #     cls, func, data_gen, gen_min_arg, gen_max_arg, gen_steps, iterations=1
    # ):
    # best_asymptotic_fit, _ = big_o(
    #     func=func,
    #     data_generator=data_gen,
    #     min_n=gen_min_arg,
    #     max_n=gen_max_arg,
    #     n_measures=gen_steps,
    #     n_repeats=iterations,
    # )
    # self.print_title("TIME BIG O")
    # self.print_function(func)
    # print(best_asymptotic_fit)

    # def run_memory_big_o(
    #     cls, func, data_gen, gen_min_arg, gen_max_arg, gen_steps, iterations=1
    # ):
    # self.print_title("MEMORY BIG O")
    # self.print_function(func)

    # data_gen_args = np.linspace(gen_min_arg, gen_max_arg, gen_steps).astype("int64")
    # mem_usages = np.empty(gen_steps)

    # for index, data_gen_arg in enumerate(data_gen_args):
    #     mem_usage = 0
    #     func_arg = data_gen(data_gen_arg)

    #     # for _ in range(iterations):
    #     mem_usage = cls._get_mem_usage(func, func_arg)

    #     mem_usages[index] = mem_usage

    # data_gen_args = data_gen_args / 1000

    # best, _ = infer_big_o_class(
    #     data_gen_args, mem_usages, ALL_CLASSES, verbose=False
    # )
    # print(best)

    # # print(data_gen_args)
    # # print(mem_usages)

    # from matplotlib import pyplot as plt

    # plt.plot(data_gen_args, mem_usages)
    # plt.show()

    # coeff, residuals, rank, s = np.linalg.lstsq(data_gen_args, mem_usages, rcond=-1)
