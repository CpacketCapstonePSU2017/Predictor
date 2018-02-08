import unittest
from unittest.mock import patch
from pframework import TrafficPredictor


class TesterPframeworkSelector(unittest.TestCase):
    predictor = TrafficPredictor()

    @patch('builtins.input')
    def test_selecting_model_test(self, mocked_input):
        try:
            mocked_input.side_effect = ['0','n']
            self.predictor.main()
        except Exception as error:
            self.fail("Test: Failed - {0}\n".format(error))

    def test_importing_model_test(self):
        try:
            result = self.predictor.call_model('SimpleMovingAverage')
            self.assertIsNotNone(result)
        except Exception as error:
            self.fail("Test: Failed - {0}\n".format(error))

    def test_importing_wrong_model(self):
            with self.assertRaises(TypeError):
                self.predictor.call_model('model_test_1')

