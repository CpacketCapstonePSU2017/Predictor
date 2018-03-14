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

    def test_holt_winters_functions(self):
        alpha = 0.716
        beta = 0.029
        gamma = 0.993
        num_predictions = 24
        series_length = 12
        series = [30, 21, 29, 31, 40, 48, 53, 47, 37, 39, 31, 29, 17, 9, 20, 24, 27, 35, 41, 38,
                  27, 31, 27, 26, 21, 13, 21, 18, 33, 35, 40, 36, 22, 24, 21, 20, 17, 14, 17, 19,
                  26, 29, 40, 31, 20, 24, 18, 26, 17, 9, 17, 21, 28, 32, 46, 33, 23, 28, 22, 27,
                  18, 8, 17, 21, 31, 34, 44, 38, 31, 30, 26, 32]
        known_trend = -0.7847222222222222
        known_seasonal_data = [-7.4305555555555545, -15.097222222222221, -7.263888888888888, -5.097222222222222,
                               3.402777777777778, 8.069444444444445, 16.569444444444446, 9.736111111111112,
                               -0.7638888888888887, 1.902777777777778, -3.263888888888889, -0.7638888888888887]
        known_predicted_data = [22.42511411230803, 15.343371755223066, 24.14282581581347, 27.02259921391996,
                                35.31139046245393, 38.999014669337356, 49.243283875692654, 40.84636009563803,
                                31.205180503707012, 32.96259980122959, 28.5164783238384, 32.30616336737171,
                                22.737583867810464, 15.655841510725496, 24.4552955713159, 27.33506896942239,
                                35.62386021795636, 39.31148442483978, 49.55575363119508, 41.15882985114047,
                                31.517650259209443, 33.275069556732014, 28.82894807934083, 32.618633122874144]

        # dummy needed to call functions
        HW = hw.HoltWinters()

        # exercise initial_trend() function with known series data and result
        test_trend = HW.initial_trend(series, series_length)
        self.assertEqual(known_trend, test_trend)

        # exercise initial_seasonal_components() function with known series data and result
        test_seasonal_component = HW.initial_seasonal_components(series, series_length)
        count = 0
        result = 0
        for i in known_seasonal_data:
            if i != test_seasonal_component[count]:
                result = -1
                break
            else:
                count += 1
        self.assertEqual(result, 0, "Compared lists are not equal ")

        # exercise triple_exponential_smoothing function with known series data and result
        test_triple_smoothing = HW.triple_exponential_smoothing(series, series_length, alpha, beta, gamma,
                                                                num_predictions)
        count = 0
        result = 0
        for i in known_predicted_data:
            if i != test_triple_smoothing[count]:
                result = -1
                break
            else:
                count += 1
        self.assertEqual(result, 0, "Compared lists are not equal ")

    def test_call_model(self):
        HW = hw.HoltWinters()
        result = HW.call_model()

        # verify predicted array isn't empty
        self.assertIsNotNone(result)

        # verify dimension and size of array
        self.assertEqual(2, result.ndim)
        self.assertEqual((HW.default_num_predictions * result.ndim), result.size)
