import importlib
import inspect
import os

from coverage import Coverage

from .helpers import LabelBase
from .printers import TablePrinterMixin
from .schema_check import SchemaCheckMixin


class CoverageLabels(LabelBase):
    FULLY_COVERED = "Function is 100% test covered."
    MISSING_STMTS = "There are missing lines."
    STMTS = "Statements"
    MISSED_STMTS = "Missed"
    COVER = "Cover"


class CoverageCheck(SchemaCheckMixin, TablePrinterMixin):
    def __init__(self, func, test_set):
        self.validate_test_set_schema(test_set)
        self.test_set = test_set
        self.func = func
        self.coverage = self.init_coverage_obj()

    @property
    def func_file_path(self):
        func_path = inspect.getfile(self.func)
        return os.path.abspath(func_path)

    @property
    def func_file_dir(self):
        return os.path.dirname(self.func_file_path)

    @property
    def temp_dir(self):
        return os.path.join(os.path.dirname(__file__), "temp_files")

    def init_coverage_obj(self):
        coverage = Coverage(
            data_file=None,
            config_file=False,
            auto_data=False,
            source=[self.func_file_dir],
            include=self.func_file_path,
            timid=True,
        )
        coverage._no_warn_slugs = ["include-ignored"]
        return coverage

    def run_coverage(self):
        self.coverage.start()
        # Because function module was imported before, we reload it to get the full coverage.
        importlib.reload(inspect.getmodule(self.func))

        for test_data in self.test_set:
            self.func(**test_data["input"])

        self.coverage.stop()

    def check_coverage(self):
        analysis_result = self.coverage.analysis(self.func_file_path)
        missing_stmts = analysis_result[2]
        return len(missing_stmts) == 0

    def print_summary(self):
        _, stmts, missing_stmts, _ = self.coverage.analysis(morf=self.func_file_path)
        stmts_num = len(stmts)
        missing_stmts_num = len(missing_stmts)
        cov_percent = round((stmts_num - missing_stmts_num) / stmts_num * 100)
        cov_label = f"{cov_percent}%"

        col_names = [
            CoverageLabels.STMTS,
            CoverageLabels.MISSED_STMTS,
            CoverageLabels.COVER,
        ]
        col_values = [stmts_num, missing_stmts_num, cov_label]

        self.print_table([col_names, col_values])
        print("")

    def print_annotations(self):
        self.coverage.annotate(morfs=self.func_file_path, directory=self.temp_dir)
        files = os.listdir(self.temp_dir)
        annotate_file_name = list(
            filter(lambda name: name.endswith(".py,cover"), files)
        )[0]
        annotate_file_path = os.path.join(self.temp_dir, annotate_file_name)
        with open(annotate_file_path, "r") as annotate_file:
            print(annotate_file.read())
        os.remove(annotate_file_path)

    def print_result(self):
        is_covered = self.check_coverage()

        if is_covered:
            print(f"\n{CoverageLabels.FULLY_COVERED}")
        else:
            print(f"\n{CoverageLabels.MISSING_STMTS}\n")
            self.print_summary()
            self.print_annotations()

    def test_coverage(self):
        self.run_coverage()
        self.print_result()
