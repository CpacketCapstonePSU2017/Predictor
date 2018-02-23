import numpy as np
import pandas as pd
from csv_to_dataframe import csv_to_dataframe
from resources.config import RESOURCES_DIR
import os

class HoltWinters:

    def __init__(self, series, slen, alpha, beta, gamma, n_preds, csv_filename):
        self.default_series = series
        self.default_stride_length = slen
        self.default_alpha = alpha
        self.default_beta = beta
        self.default_gamma = gamma
        self.default_num_predictions = n_preds
        self.default_csv_filename = os.path.join(RESOURCES_DIR, csv_filename)

    def initial_trend(Self, series, slen):
        sum = 0.0
        for i in range(slen):
            sum += float(series[i + slen] - series[i]) / slen
        return sum / slen

    def initial_seasonal_components(Self, series, slen):
        seasonals = {}
        season_averages = []
        n_seasons = int(len(series) / slen)
        # compute season averages
        for j in range(n_seasons):
            season_averages.append(sum(series[slen * j:slen * j + slen]) / float(slen))
        # compute initial values
        for i in range(slen):
            sum_of_vals_over_avg = 0.0
            for j in range(n_seasons):
                sum_of_vals_over_avg += series[slen * j + i] - season_averages[j]
            seasonals[i] = sum_of_vals_over_avg / n_seasons
        return seasonals

    def triple_exponential_smoothing(self, series, slen, alpha, beta, gamma, n_preds):
        result = []
        seasonals = self.initial_seasonal_components(series, slen)
        for i in range(len(series) + n_preds):
            if i == 0:  # initial values
                smooth = series[0]
                trend = self.initial_trend(series, slen)
                result.append(series[0])
                continue
            if i >= len(series):  # we are forecasting
                m = i - len(series) + 1
                result.append((smooth + m * trend) + seasonals[i % slen])
            else:
                val = series[i]
                last_smooth, smooth = smooth, alpha * (val - seasonals[i % slen]) + (1 - alpha) * (smooth + trend)
                trend = beta * (smooth - last_smooth) + (1 - beta) * trend
                seasonals[i % slen] = gamma * (val - smooth) + (1 - gamma) * seasonals[i % slen]
                result.append(smooth + trend + seasonals[i % slen])
        return result

    def call_model(self):
        # build dataframe
        # FIXME: Remove this code to use csv_to_dataframe. This is sample data from Holt-Winters blog
        series = [30, 21, 29, 31, 40, 48, 53, 47, 37, 39, 31, 29, 17, 9, 20, 24, 27, 35, 41, 38,
                  27, 31, 27, 26, 21, 13, 21, 18, 33, 35, 40, 36, 22, 24, 21, 20, 17, 14, 17, 19,
                  26, 29, 40, 31, 20, 24, 18, 26, 17, 9, 17, 21, 28, 32, 46, 33, 23, 28, 22, 27,
                  18, 8, 17, 21, 31, 34, 44, 38, 31, 30, 26, 32]
        self.default_series = series
        self.default_stride_length = 12
        self.default_num_predictions = 24

        # FIXME: fix this code, causing error: TypeError: unsupported operand type(s) for +: 'int' and 'str'
        #df = csv_to_dataframe(self.default_csv_filename, 0, 21, False, [1])
        #self.default_series = df
        #self.default_stride_length = 4

        # pick desired seasonal length, alpha, beta, gamma and desired number of predicted points

        # call triple_exponential_smoothing with series = byte counts column in dataframe
        smooth_series = self.triple_exponential_smoothing(self.default_series, self.default_stride_length,
                                                          self.default_alpha, self.default_beta, self.default_gamma,
                                                          self.default_num_predictions)
        # FIXME: debug print code, remove
        print(smooth_series)
        print(len(smooth_series))

        # pass back series with N new predicted results
        # generate N new new sequential timestamps (per 15 min)
        # assign new timestamps to datapoints
        # append new timestamp:datapoint pairs to original dataframe
        # pass back completed dataframe or generate new csv file.
        return 1


# FIXME: Remove this test code at end. Only for testing class
test = HoltWinters(None, 4, 0.716, 0.029, 0.993, 4, 'temp.csv')
test.call_model()
