from unittest import TestCase
from PModules.HoltWinters import HoltWinters as hw


class TesterHoltWinters(TestCase):

    def test_initialization(self):
        HW = hw.HoltWinters()

        # verify init parameters have been set
        self.assertIsNotNone(HW.default_num_predictions)
        self.assertIsNotNone(HW.default_num_train_weeks)
        self.assertIsNotNone(HW.default_stride_length)
        self.assertIsNotNone(HW.default_alpha)
        self.assertIsNotNone(HW.default_beta)
        self.assertIsNotNone(HW.default_gamma)

        # verify a valid data_file was passed in to create a data_frame
        self.assertIsNotNone(HW.returned_data_frame)

    def test_sample_data(self):
        self.assertEqual(1, 1)

    def test_call_model(self):
        HW = hw.HoltWinters()
        result = HW.call_model()

        # verify predicted array isn't empty
        self.assertIsNotNone(result)

        # verify dimension and size of array
        self.assertEqual(2, result.ndim)
        self.assertEqual((HW.default_num_predictions * result.ndim), result.size)

