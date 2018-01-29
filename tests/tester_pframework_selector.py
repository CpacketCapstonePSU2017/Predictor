import unittest
from unittest.mock import patch
from pframework import TrafficPredictor


class MyTestCase(unittest.TestCase):
    predictor = TrafficPredictor()

    @patch('builtins.input')
    def test_selecting_model_test(self, mocked_input):
        try:
            mocked_input.side_effect = ['0']
            self.predictor.main()
        except Exception as error:
            self.fail("Test: Failed - {0}\n".format(error))

    def test_importing_model_test(self):
        try:
            result = self.predictor.call_model('model_test')
            self.assertEqual(result, "This is model test!")
        except Exception as error:
            self.fail("Test: Failed - {0}\n".format(error))

    def test_importing_wrong_model(self):
        try:
            result = self.predictor.call_model('model_test_1')
            self.assertEqual(result, None)
        except Exception as error:
            self.fail("Test: Failed - {0}\n".format(error))


