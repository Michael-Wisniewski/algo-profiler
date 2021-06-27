import io
from unittest import TestCase, mock

from src.big_o_analyzer import BigOLabels, extend_analyse


class TestBigOAnalyzer(TestCase):
    def test_run_with_two_points(self):
        args = [1, 1]
        vals = [1, 1]

        with self.assertRaises(ValueError) as context:
            extend_analyse(args=args, vals=vals)

        self.assertEqual(str(context.exception), str(BigOLabels.NOT_ENOUGH_POINTS))

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_run_with_three_points(self, mock_stdout):
        args = [1, 2, 3]
        vals = [10000, 80000, 270000]
        extend_analyse(args=args, vals=vals)

        self.assertIn("Best fitted function:\n\nCubic", mock_stdout.getvalue())

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_run_with_small_vals(self, mock_stdout):
        args = [100, 200, 300, 400, 500, 600, 700]
        vals = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007]
        extend_analyse(args=args, vals=vals)

        self.assertIn("Best fitted function:\n\nLinear", mock_stdout.getvalue())

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_run_with_big_args(self, mock_stdout):
        args = [10000000, 20000000, 30000000, 40000000, 50000000, 60000000]
        vals = [1, 2, 3, 4, 5, 6]
        extend_analyse(args=args, vals=vals)

        self.assertIn("Best fitted function:\n\nLinear", mock_stdout.getvalue())
