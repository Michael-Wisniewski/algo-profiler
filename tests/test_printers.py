import io
from textwrap import dedent
from unittest import TestCase, mock

from src.printers import PrinterMixin, TablePrinterMixin


class TestPrinterMixin(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.printer = PrinterMixin()

    @property
    def test_func(self):
        def func(a, b):
            pass

        return func

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_print_title(self, mock_stdout):
        expected_title = "\n\x1b[1m\x1b[47m\x1b[34m   TITLE   \x1b[0m\n\n"
        self.printer.print_title("TITLE")
        self.assertEqual(dedent(mock_stdout.getvalue()), expected_title)

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_print_function(self, mock_stdout):
        expected_function = "Function: \x1b[1m\x1b[34mfunc(a, b)\x1b[0m\n"
        self.printer.print_function(self.test_func)
        self.assertEqual(mock_stdout.getvalue(), expected_function)

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_print_kwargs(self, mock_stdout):
        expected_kwargs = (
            "\n\x1b[1m\x1b[34mtest_list\x1b[0m(4): [1, 2, 3, 4]\n"
            "\x1b[1m\x1b[34mtest_dict\x1b[0m(1): {'key': 'value'}\n"
            "\x1b[1m\x1b[34mtest_var\x1b[0m: 1\n\n"
        )
        kwargs = {
            "test_list": [1, 2, 3, 4],
            "test_dict": {"key": "value"},
            "test_var": 1,
        }
        self.printer.print_kwargs(kwargs)
        self.assertEqual(mock_stdout.getvalue(), expected_kwargs)

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_print_kwargs_with_size(self, mock_stdout):
        expected_kwargs = (
            "\n\x1b[1m\x1b[34mtest_list\x1b[0m(4) 0.0002 MB: [1, 2, 3, 4]\n"
            "\x1b[1m\x1b[34mtest_dict\x1b[0m(1) 0.0003 MB: {'key': 'value'}\n"
            "\x1b[1m\x1b[34mtest_var\x1b[0m 0.0 MB: 1\n\n"
        )
        kwargs = {
            "test_list": [1, 2, 3, 4],
            "test_dict": {"key": "value"},
            "test_var": 1,
        }
        self.printer.print_kwargs(kwargs, show_size=True)
        self.assertEqual(mock_stdout.getvalue(), expected_kwargs)


class TestTablePrinterMixin(TestCase):
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_printing_table(self, mock_stdout):
        expected_table = dedent(f"""\
        First               Second              Third               Fourth              
        --------------------------------------------------------------------------------
        a                   b                   c                   d                   
        --------------------------------------------------------------------------------
        1                   2                   3                   4                   
        --------------------------------------------------------------------------------
        
        """
        )

        col_names = ["First", "Second", "Third", "Fourth"]
        first_row = ["a", "b", "c", "d"]
        second_row = [1, 2, 3, 4]
        rows = [col_names, first_row, second_row]

        table_printer = TablePrinterMixin()
        table_printer.print_table(rows)

        self.assertTrue(mock_stdout.getvalue(), expected_table)
