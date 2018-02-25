import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import io_framework.csv_to_dataframe as cdf
from resources.config import RESOURCES_DIR
import os
import math

class ExpSmoothing:

    def __init__(self, series, alpha, csv_filename):
        self.default_series = series
        self.default_alpha = alpha
        self.default_csv_filename = os.path.join(RESOURCES_DIR, csv_filename)

    def gen_weights(self, alpha, number_of_weights):
        ws =list()
        for i in range(number_of_weights):
            w = alpha * ((1-alpha)**i)
            ws.append(w)
        return ws

    #def weighted(self):
    # given a series and alpha, return series of smoothed points
    def exponential_smoothing(self, series, alpha):
        result = [series[0]]  # first value is same as series
        length = len(series)
        weeks_to_count = math.floor(length/672)
        weights = self.gen_weights(alpha, weeks_to_count)
        if weeks_to_count is 0:
            print("Not enough data!")
            return False
        for n in range(1, len(series)):
            result.append(alpha * series[n-672] + (1 - alpha) * series[n])
        return result

    # >>> exponential_smoothing(series, 0.1)
    # [3, 3.7, 4.53, 5.377, 6.0393, 6.43537, 6.991833]
    # >>> exponential_smoothing(series, 0.9)
    # [3, 9.3, 11.73, 12.873000000000001, 12.0873, 10.20873, 11.820873]


    def call_model(self):
        # build dataframe
        df = cdf.csv_to_dataframe("/home/pirate/Desktop/AccessPoint1Incoming.csv", 0, 29474, False, [1])
        series = list(df.values.flatten())
        # FIXME: remove debug code
        print(series)
        print(len(series))  # pick desired seasonal length, alpha, beta, gamma and desired number of predicted points
        self.default_series = series  # call triple_exponential_smoothing with series = byte counts column in dataframe
        smooth_series = self.exponential_smoothing(self.default_series, self.default_alpha)
        # FIXME: remove debug code
        print(smooth_series)
        print(len(smooth_series))
        #plt.plot(smooth_series)
        #plt.ylabel('some numbers')
        #plt.show()  # pass back series with N new predicted results
        # generate N new new sequential timestamps (per 15 min)
        # assign new timestamps to datapoints
        # append new timestamp:datapoint pairs to original dataframe
        # pass back completed dataframe or generate new csv file.
        return 1  # FIXME: Remove this test code at end. Only for testing class


test = ExpSmoothing(None, 0.75, 'temp.csv')
test.call_model()
