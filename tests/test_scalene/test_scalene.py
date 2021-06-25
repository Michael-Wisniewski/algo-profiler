from .functions import sleep_miliseconds
from unittest import TestCase, mock
from src.scalene_analyzer import scalene_analyzer


class TestScalene(TestCase):
    def test_removing_the_right_files(self):
        temp_files_paths = []

        scalene_analyzer(func=sleep_miliseconds, kwargs={"n": 1000})

        # with mock.patch("os.remove") as mock_remove:
        #     scalene_analyzer(func=create_list, kwargs={"n": 4})
        #     temp_files_paths = mock_remove.call_args_list

        # import pdb
        # pdb.set_trace()
