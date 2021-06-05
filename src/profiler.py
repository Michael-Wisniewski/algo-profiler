import cProfile
import inspect

from line_profiler import LineProfiler

from .coverage_check import CoverageCheck
from .memory_check import MemoryCheck
from .printers import PrinterMixin
from .tester import Tester
from .timer import Timer
from pympler import tracker


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

    def run_time_analysis(
        self,
        func,
        data_gen,
        gen_min_arg,
        gen_max_arg,
        gen_steps,
        iterations,
        draw_chart=False,
    ):
        self.print_title("TIMER")
        self.print_function(func)
        self.timer.run_time_analysis(
            func=func,
            data_gen=data_gen,
            gen_min_arg=gen_min_arg,
            gen_max_arg=gen_max_arg,
            gen_steps=gen_steps,
            iterations=iterations,
            draw_chart=draw_chart,
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
        self.memory_check.run_memory_check(func=func, kwargs=kwargs)

    def run_memory_profiler(self, func, kwargs, clean_result=False):
        self.print_title("MEMORY PROFILER")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        self.memory_check.run_memory_profiler(func=func, kwargs=kwargs, clean_result=clean_result)

    def run_time_based_memory_usge(self, func, kwargs, interval=0.1):
        self.print_title("TIME BASED MEMORY USAGE")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        self.memory_check.run_time_based_memory_usge(func=func, kwargs=kwargs, interval=interval)

    def run_memory_analysis(
        self,
        func,
        data_gen,
        gen_min_arg,
        gen_max_arg,
        gen_steps,
        draw_chart=False,
    ):
        self.print_title("MEMORY CHECKS")
        self.print_function(func)
        self.memory_check.run_memory_analysis(
            func=func,
            data_gen=data_gen,
            gen_min_arg=gen_min_arg,
            gen_max_arg=gen_max_arg,
            gen_steps=gen_steps,
            draw_chart=draw_chart,
        )

    def check_memory_leaks(self, func, kwargs, num_of_checks=3):
        self.print_title("MEMORY LEAK CHECK")
        self.print_function(func)
        self.print_kwargs(kwargs, show_size=True)
        tr = tracker.SummaryTracker()
        func(**kwargs)

        for i in range(1, num_of_checks + 1):
            self.print_title(f"MEMORY CONTROL AT THE END OF THE FUNCTION #{i}")
            tr.print_diff()
        
        print()

    # dodac scalane i porownac dla func i naive_func
    # dodac hype

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


    def run_big_o_time_check(
        self,
        func,
        data_gen,
        gen_min_arg,
        gen_max_arg,
        gen_steps,
        iterations=1,
        verbose=False
    ):
        self.print_title("TIME BIG O COMPLEXITY")
        self.print_function(func)


        # from big_o import big_o, infer_big_o_class
        # from big_o.complexities import ALL_CLASSES  
       
        def func_wrapper(kwargss):
            return func(**kwargss)


        from big_o import big_o

        best, others = big_o(
            func=func_wrapper,
            data_generator=data_gen,
            min_n=gen_min_arg,
            max_n=gen_max_arg,
            n_measures=gen_steps,
            n_repeats=4,
            n_timings=iterations,
            # classes=ALL_CLASSES,
            verbose=False,
            return_raw_data=False,
        )

        print(best)
        print(others)
