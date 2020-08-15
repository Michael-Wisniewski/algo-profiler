from unittest import TestCase

from src.helpers import LabelBase


class LabelBaseTest(TestCase):
    def test_printing_labels(self):
        class TestLabelClass(LabelBase):
            TEST_LABEL = "TEST LABEL TEXT"

        self.assertEqual(str(TestLabelClass.TEST_LABEL), TestLabelClass.TEST_LABEL.value)
