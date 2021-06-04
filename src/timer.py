from timeit import timeit

import matplotlib.pyplot as plt

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

    def __init__(self, runs_num):
        self.runs_num = runs_num
        self.results = []
        self.print_headers()

    def print_headers(self):
        column_names = [
            TimerLabels.RUN_NUMBER,
            TimerLabels.RUN_ARGUMENT,
            TimerLabels.RUN_TIME,
        ]
        self.print_row(columns=column_names, column_width=self.column_width)

    def append(self, run_idnex, run_arg, run_time):
        self.results.append({"arg": run_arg, "time": run_time})
        counter = f"{run_idnex}/{self.runs_num}"
        columns_value = [counter, run_arg, run_time]
        self.print_row(columns=columns_value, column_width=self.column_width)

        if run_idnex == self.runs_num:
            print("")

    def draw_chart(self):
        plt.title("Function run times")
        plt.xlabel("Data generator's argument")
        plt.ylabel("Measured time")

        x = [result["arg"] for result in self.results]
        y = [result["time"] for result in self.results]

        plt.plot(x, y)
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
    ):
        print(f"{TimerLabels.RUN_ITERATIONS}: {iterations}\n\n")
        args = linear_space(
            min_val=gen_min_arg, max_val=gen_max_arg, steps_num=gen_steps
        )
        result_formatter = TimerResultFormatter(runs_num=len(args))

        for index, arg in enumerate(args):
            data = data_gen(arg)
            run_time = self.get_run_time(func=func, kwargs=data, iterations=iterations)
            result_formatter.append(run_idnex=index + 1, run_arg=arg, run_time=run_time)

        if draw_chart:
            result_formatter.draw_chart()
