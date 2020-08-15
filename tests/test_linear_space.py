import io
from unittest import TestCase, mock

from parameterized import parameterized

from src.linear_space import linear_space


class TestLinearSpace(TestCase):
    @parameterized.expand([
        (0, 0, 1, [0]),
        (1, 1, 1, [1]),
        (100, 100, 1, [100])
    ])
    def test_one_available_point(self, min_val, max_val, steps_num, result):
        self.assertEqual(linear_space(min_val, max_val, steps_num), result)

    @parameterized.expand([
        (0, 10, 1, [0]),
        (1, 10, 1, [1]),
        (1, 100, 1, [1])
    ])
    def test_one_generated_point(self, min_val, max_val, steps_num, result):
        self.assertEqual(linear_space(min_val, max_val, steps_num), result)

    @parameterized.expand([
        (0, 10, 1, [0]),
        (0, 10, 2, [0, 10]),
        (0, 10, 3, [0, 5, 10]),
        (0, 10, 4, [0, 3, 6, 9]),
        (0, 10, 5, [0, 2, 4, 6, 8]),
        (0, 10, 6, [0, 2, 4, 6, 8, 10]),
        (0, 10, 7, [0, 1, 2, 3, 4, 5, 6]),
        (0, 10, 8, [0, 1, 2, 3, 4, 5, 6, 7]),
        (0, 10, 9, [0, 1, 2, 3, 4, 5, 6, 7, 8]),
        (0, 10, 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (0, 10, 11, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    ])
    def test_range_from_0_to_10(self, min_val, max_val, steps_num, result):
        self.assertEqual(linear_space(min_val, max_val, steps_num), result)

    @parameterized.expand([
        ("1", 1, 1),
        (1, "1", 1),
        (1, 1, "1"),
        (-1, 1, 1),
        (1, -1, 1),
        (1, 1, -1)
    ])
    def test_wrong_argument_type_or_value(self, min_val, max_val, steps_num):
        with self.assertRaises(TypeError) as context: 
            linear_space(min_val, max_val, steps_num)

        self.assertEqual(str(context.exception), "All arguments have to be positive integers.")

    def test_wrong_argument_range(self):
        with self.assertRaises(ValueError) as context: 
            linear_space(min_val=1, max_val=0, steps_num=1)

        self.assertEqual(str(context.exception), "Maximal argument can not be smaller than minimal.")

    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_too_much_steps(self, mock_stdout):
        result = linear_space(min_val=1, max_val=10, steps_num=15)

        self.assertEqual(
            mock_stdout.getvalue(),
            "Warning: number of steps was reduced to maximum available value for range <1,10> to 10.\n"
        )
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
