import numpy as np
import pandas as pd
#import matplotlib.pyplot
import io_framework.csv_to_dataframe as cdf
from resources.config import RESOURCES_DIR
import os
import math

class ExpSmoothing:

    def __init__(self, series, alpha, csv_filename):
        """
        The parameters for this function are:
        :param series: The series passed in from call model.
        :param alpha: The alpha for N.
        :param csv_filename: The name of the CSV file with the series data.
        """
        self.default_series = series
        self.default_alpha = alpha
        self.default_csv_filename = os.path.join(RESOURCES_DIR, csv_filename)

    def gen_weights(self, alpha, number_of_weights):
        """
        The parameters for a function that generates weights:
        :param alpha: The alpha for N.
        :param number_of_weights: The amount of weeks observed in the data.
        :return: A list the size of number_of_weights with weights from alpha that approach 0.
        """
        ws =list()
        for i in range(number_of_weights):
            w = alpha * ((1-alpha)**i)
            ws.append(w)
        return ws

    def exponential_smoothing(self, series, alpha):
        """
        The parameters to make an exponential smoothing prediction
        :param series: This is the series that is passed in from main that has the data to be processed.
        :param alpha: The starting weight.
        :return:
        """
        result = [series[0]]  # first value is same as series
        length = len(series)
        weeks_to_count = math.floor(length/672)
        weights = self.gen_weights(alpha, weeks_to_count)
        ex_weights = self.gen_weights(alpha, weeks_to_count+1)
        excess = length % 672

        if weeks_to_count is 0:
            print("Not enough data!")
            return False
        for n in range(0, 672):
            total = 0
            if excess > n:
                for i in range(weeks_to_count, 0, -1):
                    wght = ex_weights[i]
                    offset = n + (i * 672)
                    data = series[offset]
                    total = total + (wght * data)
                result.append(total)
            else:
                for i in range(weeks_to_count - 1, 0, -1):
                    wght = weights[i]
                    offset = n + (i * 672)
                    data = series[offset]
                    total = total + (wght * data)
                result.append(total)
        return result

    def call_model(self):
        # build dataframe
        df = cdf.csv_to_dataframe(self.default_csv_filename,0,34945 , False, [0,1])
        series = list(df.values.flatten())
        bytcts = series[1::2]
        self.default_series = bytcts  # call triple_exponential_smoothing with series = byte counts column in dataframe
        smooth_series = self.exponential_smoothing(self.default_series, self.default_alpha)
        print(smooth_series)
        result_datetimes = pd.date_range(series[-2], periods=674, freq='15min')[1:]
        nparray_data = np.array([result_datetimes, smooth_series]).transpose()

        #print(nparray_data)
        #print(nparray_data[670][0])
        #print(nparray_data[670][1])
        #print(len(nparray_data))
        #matplotlib.pyplot.plot(smooth_series)
        #matplotlib.pyplot.ylabel('some numbers')
        #matplotlib.pyplot.show()  # pass back series with N new predicted results

        return nparray_data


test = ExpSmoothing(None, 0.2, "/home/pirate/Desktop/AccessPoint1Incoming.csv")
test.call_model()
