from timeit import timeit

import matplotlib.pyplot as plt

from .big_o_analyzer import extend_analyse
from .helpers import LabelBase
from .linear_space import linear_space
from .printers import TablePrinterMixin


class TimerLabels(LabelBase):
    RUN_NUMBER = "Run number"
    RUN_ARGUMENT = "Function argument"
    RUN_ITERATIONS = "Function iterations"
    RUN_TIME = "Avg time (sec)"


class TimerResultFormatter(TablePrinterMixin):
    column_width = 23

    def __init__(self, runs_num, func_name):
        self.runs_num = runs_num
        self.func_name = func_name
        self.args = []
        self.time = []
        self.print_headers()

    def print_headers(self):
        column_names = [
            TimerLabels.RUN_NUMBER,
            TimerLabels.RUN_ARGUMENT,
            TimerLabels.RUN_TIME,
        ]
        self.print_row(columns=column_names, column_width=self.column_width)

    def append(self, run_idnex, run_arg, run_time):
        self.args.append(run_arg)
        self.time.append(run_time)
        counter = f"{run_idnex}/{self.runs_num}"
        columns_value = [counter, run_arg, run_time]
        self.print_row(columns=columns_value, column_width=self.column_width)

        if run_idnex == self.runs_num:
            print("")

    def render_base_chart(self):
        plt.title("Function run times")
        plt.xlabel("Data generator's argument")
        plt.ylabel("Time [s]")
        func_label = f"{self.func_name} function"
        plt.plot(self.args, self.time, label=func_label)

    def render_extended_chart(self):
        extend_analyse(args=self.args, vals=self.time, plt=plt)

    def display_chart(self):
        plt.legend()
        plt.show()


class Timer:
    def get_run_time(self, func, kwargs, iterations=1):
        total_execution_time = timeit(lambda: func(**kwargs), number=iterations)
        avg_execution_time = total_execution_time / iterations
        return avg_execution_time

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
        print(f"{TimerLabels.RUN_ITERATIONS}: {iterations}\n\n")
        args = linear_space(
            min_val=gen_min_arg, max_val=gen_max_arg, steps_num=gen_steps
        )
        result_formatter = TimerResultFormatter(
            runs_num=len(args), func_name=func.__name__
        )

        for index, arg in enumerate(args):
            data = data_gen(arg)
            run_time = self.get_run_time(func=func, kwargs=data, iterations=iterations)
            result_formatter.append(run_idnex=index + 1, run_arg=arg, run_time=run_time)

        if find_big_o:
            result_formatter.render_base_chart()
            result_formatter.render_extended_chart()
            result_formatter.display_chart()
        elif draw_chart:
            result_formatter.render_base_chart()
            result_formatter.display_chart()
