import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io_framework.csv_fill_data_gaps as fg
from io_framework.csv_writer import CsvWriter
from predictor_resources.config import RESOURCES_DIR
from os import path
import datetime

class HoltWinters:

    def __init__(self, series, n_preds, slen=672, alpha=0.816, beta=0.0001, gamma=0.993, data_file="AccessPoint#3(Aruba3)Outgoing.csv"):
        self.default_series = series
        self.default_stride_length = slen
        self.default_alpha = alpha
        self.default_beta = beta
        self.default_gamma = gamma
        self.default_num_predictions = n_preds
        self.data_column_name = ""
        self.csvWriter = CsvWriter(host="", port=0, username="", password="", database="", new_measurement="", new_cvs_file_name="")
        self.returned_data_frame = self.csvWriter.csv_file_to_dataframe(new_filepath=path.join(RESOURCES_DIR, data_file), new_row_start=0) # change this hard code

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
        result = list()
        seasonals = self.initial_seasonal_components(series, slen)
        for i in range(len(series) + n_preds):
            if i == 0:  # initial values
                smooth = series[0]
                trend = self.initial_trend(series, slen)
                result.append(float(series[0]))
                continue
            if i >= len(series):  # we are forecasting
                m = i - len(series) + 1
                new_level = (smooth + m * trend) + float(seasonals[i % slen])
                new_level = float(0) if new_level < 0 else new_level
                result.append(new_level)
            else:
                val = series[i]
                last_smooth, smooth = smooth, alpha * (val - seasonals[i % slen]) + (1 - alpha) * (smooth + trend)
                trend = beta * (smooth - last_smooth) + (1 - beta) * trend
                seasonals[i % slen] = gamma * (val - smooth) + (1 - gamma) * seasonals[i % slen]
                #result_to_append = smooth + trend + seasonals[i % slen]
                #result = np.append(result, result_to_append)
        return result

    def call_model(self):
        # build dataframe
        df = fg.fill_data_gaps(self.returned_data_frame.shape[0], init_data=self.returned_data_frame)
        df['avg_hrcrx_max_byt'] = df['avg_hrcrx_max_byt'].fillna(0)

        # create n array from dataframe
        tmp_series = list(df.values.flatten())
        self.default_series = tmp_series[1::2]

        # call triple_exponential_smoothing with series = byte counts column in dataframe
        smooth_series = self.triple_exponential_smoothing(self.default_series, self.default_stride_length,
                                                          self.default_alpha, self.default_beta, self.default_gamma,
                                                          self.default_num_predictions)
        combined_data = np.append(self.default_series, smooth_series)

        # generate N new new sequential timestamps (per 15 min)
        start_date = datetime.date.today()
        result_datetimes = pd.date_range(start_date, periods=len(smooth_series), freq='15min')[0:]

        # assign new timestamps to datapoints
        nparray_data = np.array([result_datetimes, smooth_series]).transpose()

        # pass back completed dataframe or generate new csv file.
        return nparray_data

    def get_data_column_name(self):
        return self.data_column_name

