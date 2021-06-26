import io

from unittest import TestCase, mock
from src.big_o_analyzer import extend_analyse, BigOLabels


class TestBigOAnalyzer(TestCase):
    # def test_run_with_two_points(self):
    #     args = [1, 1]
    #     vals = [1, 1]

    #     with self.assertRaises(ValueError) as context:
    #         extend_analyse(args=args, vals=vals)

    #     self.assertEqual(str(context.exception), str(BigOLabels.NOT_ENOUGH_POINTS))

    # @mock.patch("sys.stdout", new_callable=io.StringIO)
    # def test_run_with_three_points(self, mock_stdout):
    #     args = [1, 2, 3]
    #     vals = [10000, 80000, 270000]
    #     extend_analyse(args=args, vals=vals)

    #     self.assertIn("Best fitted function:\n\nCubic", mock_stdout.getvalue())
        
    # @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_run_with_three_points(self): #, mock_stdout):
        args = [1, 2, 3]
        vals = [10001, 10002, 10003]
        extend_analyse(args=args, vals=vals)

        # self.assertIn("Best fitted function:\n\nCubic", mock_stdout.getvalue())
