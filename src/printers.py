import os
import sys
from contextlib import contextmanager
from inspect import signature
from reprlib import Repr
from objsize import get_deep_size as get_size

# use x1b and enum
class PrinterMixin:
    def print_title(self, title):
        print("\n", (f"\033[1m\033[47m\033[34m   {title}   \033[0m\n").center(100))

    def print_function(self, func):
        print(f"Function: \033[1m\033[34m{func.__name__}{signature(func)}\033[0m")

    def print_kwargs(self, kwargs, show_size=False):
        repr_instance = Repr()
        print()

        for arg_name, arg_val in kwargs.items():
            print(f"\033[1m\033[34m{arg_name}\033[0m", end="")

            if isinstance(arg_val, (list, tuple, set, dict)):
                print(f"({len(arg_val)})", end="")

            if show_size:
                size = round(get_size(arg_val) / 1048576, 4)
                print(f" {size} MB", end="")
            
            print(f": {repr_instance.repr(arg_val)}")
        print()

class TablePrinterMixin:
    def format_columns(self, columns, column_width):
        formatted_columns = [str(column).ljust(column_width) for column in columns]
        return "".join(formatted_columns) + "\n"

    def format_horizontal_line(self, columns, column_width):
        return "-" * column_width * len(columns)

    def print_row(self, columns, column_width=20):
        row = self.format_columns(columns=columns, column_width=column_width)
        row += self.format_horizontal_line(columns=columns, column_width=column_width)
        print(row)

    def print_table(self, rows, column_width=20):
        for columns in rows:
            self.print_row(columns=columns, column_width=column_width)
