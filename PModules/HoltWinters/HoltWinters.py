import numpy as np
import pandas as pd


class HoltWinters:

    def __init__(self, series, slen, alpha, beta, gamma, n_preds):
        self.default_series = series
        self.default_stride_length = slen
        self.default_alpha = alpha
        self.default_beta = beta
        self.default_gamma = gamma
        self.default_num_preditions = n_preds

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

        # pick desired seasonal length, alpha, beta, gamma and desired number of predicted points

        # call triple_exponential_smoothing with series = byte counts column in dataframe
        # pass back series with N new predicted results
        # generate N new new sequential timestamps (per 15 min)
        # assign new timestamps to datapoints
        # append new timestamp:datapoint pairs to original dataframe
        # pass back completed dataframe or generate new csv file.
        return 1