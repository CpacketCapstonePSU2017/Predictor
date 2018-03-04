import unittest
from unittest.mock import patch
from pframework import TrafficPredictor
from influxdb import InfluxDBClient
from predictor_resources import db_config

class TesterPframeworkSelector(unittest.TestCase):
    predictor = TrafficPredictor(database='test_predicted_data')

    @patch('builtins.input')
    def test_selecting_model_test(self, mocked_input):
        print("selecting_model_test")
        try:
            mocked_input.side_effect = ['0', 'n', 'n']
            self.predictor.main()
        except Exception as error:
            self.fail("Test: Failed - {0}\n".format(error))

    @patch('builtins.input')
    def test_writing_to_db(self, mocked_input):
        print("writing_to_db")
        try:
            mocked_input.side_effect = ['0', 'n', 'y']
            self.predictor.main()
            client = InfluxDBClient(host=db_config.host, port=db_config.port, username=db_config.username,
                                    password=db_config.password, database='test_predicted_data')
            # client.create_database('test_predicted_data')
            result = client.query("select * from SimpleMovingAverage_predicted")
            self.assertIsNotNone(result)
            client.drop_database('test_predicted_data')
        except Exception as error:
            self.fail("Test: Failed - {0}\n".format(error))

    @patch('builtins.input')
    def test_importing_model_test(self, mocked_input):
        print("test_importing_model_test")
        try:
            mocked_input.side_effect = ['n']
            result = self.predictor.call_model('SimpleMovingAverage')
            self.assertIsNotNone(result)
        except Exception as error:
            self.fail("Test: Failed - {0}\n".format(error))

    def test_importing_wrong_model(self):
        with self.assertRaises(TypeError):
            self.predictor.call_model('model_test_1')

