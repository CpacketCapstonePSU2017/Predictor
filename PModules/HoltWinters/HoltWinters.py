import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import io_framework.csv_to_dataframe as cdf
from resources.config import RESOURCES_DIR
import os
import datetime

class HoltWinters:

    def __init__(self, series, slen, alpha, beta, gamma, n_preds, csv_filename):
        self.default_series = series
        self.default_stride_length = slen
        self.default_alpha = alpha
        self.default_beta = beta
        self.default_gamma = gamma
        self.default_num_predictions = n_preds
        self.default_csv_filename = os.path.join(RESOURCES_DIR, csv_filename)
        self.data_column_name = ""

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
        #df = cdf.csv_to_dataframe("/home/pirate/Desktop/AccessPoint1Incoming.csv", 0, 29474, False, [1])
        df = cdf.csv_to_dataframe(self.default_csv_filename, 0, 4, False, [1])

        # create n array from dataframe
        self.default_series = np.array(df.values.flatten())
        #FIXME: remove later
        #print(self.default_series)

        # pick desired seasonal length, alpha, beta, gamma and desired number of predicted points

        # call triple_exponential_smoothing with series = byte counts column in dataframe
        smooth_series = self.triple_exponential_smoothing(self.default_series, self.default_stride_length,
                                                          self.default_alpha, self.default_beta, self.default_gamma,
                                                          self.default_num_predictions)
        # FIXME: remove debug code
        #print(smooth_series)

        #plt.plot(smooth_series)
        #plt.ylabel('some numbers')
        #plt.show()  # pass back series with N new predicted results

        # append predicted values to known values
        # FIXME: remove debug code
        self.default_series = np.append(self.default_series, smooth_series)
        #print(self.default_series)

        # generate N new new sequential timestamps (per 15 min)
        start_date = str(datetime.date.today())
        result_datetimes = pd.date_range(start_date, periods=len(self.default_series)+1, freq='15min')[1:]
        # assign new timestamps to datapoints
        nparray_data = np.array([result_datetimes, self.default_series]).transpose()
        #self.data_column_name = self.returned_data_frame.columns[1]
        # FIXME: remove debug code
        print(nparray_data)

        # pass back completed dataframe or generate new csv file.
        return 1  # FIXME: Remove this test code at end. Only for testing class

    def get_data_column_name(self):
        return self.data_column_name


#test = HoltWinters(None, 672, 0.916, 0.929, 0.993, 1, 'AccessPoint1Incoming.csv')
test = HoltWinters(None, 2, 0.916, 0.929, 0.993, 4, 'temp.csv')
test.call_model()
