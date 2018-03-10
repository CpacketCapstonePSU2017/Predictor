import numpy as np
import pandas as pd
import io_framework.csv_fill_data_gaps as fg
from io_framework.csv_writer import CsvWriter
from predictor_resources.config import RESOURCES_DIR
from os import path

class HoltWinters:

    def __init__(self, series=None, n_preds=672, n_weeks=5, slen=672, alpha=0.816, beta=0.0001, gamma=0.993, data_file="AccessPoint#3(Aruba3)Outgoing.csv"):
        self.default_series = series
        self.default_stride_length = slen
        self.default_alpha = alpha
        self.default_beta = beta
        self.default_gamma = gamma
        self.default_num_predictions = n_preds
        self.default_num_train_weeks = n_weeks
        self.data_column_name = ""
        self.csvWriter = CsvWriter(host="", port=0, username="", password="", database="", new_measurement="", new_cvs_file_name="")
        self.returned_data_frame = self.csvWriter.csv_file_to_dataframe(new_filepath=path.join(RESOURCES_DIR, data_file), new_row_start=0) # change this hard code

    def set_parameters(self):
        """
        Asking user to change a parameters specific to a model, if needed
        :return:
        """
        print("The default number of datapoints to predict: {}".format(self.default_num_predictions))
        print("The default number of  training weeks: {}".format(self.default_num_train_weeks))
        print("The default seasonal stride length: {}".format(self.default_stride_length))
        print("The default alpha value: {}".format(self.default_alpha))
        print("The default beta value: {}".format(self.default_beta))
        print("The default gamma value: {}".format(self.default_gamma))
        print("Would you like to set the parameters for Holt-Winters first? [y]/[n]")
        selection = input("Prompt: ")
        if selection.lower() == 'y':
            print("Choose the number of datapoints to predict")
            selection = input("Prompt: ")
            self.default_num_predictions = int(selection)

            print("Choose the number of training weeks")
            selection = input("Prompt: ")
            self.default_num_train_weeks = int(selection)

            print("Choose the seasonal stride length")
            selection = input("Prompt: ")
            self.default_stride_length = int(selection)

            print("Choose the desired alpha value")
            selection = input("Prompt: ")
            self.default_alpha = float(selection)

            print("Choose the desired beta value")
            selection = input("Prompt: ")
            self.default_beta = float(selection)

            print("Choose the desired gamma value")
            selection = input("Prompt: ")
            self.default_gamma = float(selection)

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
        return result

    def call_model(self):
        # build dataframe
        df = fg.fill_data_gaps(self.returned_data_frame.shape[0], init_data=self.returned_data_frame)
        df['avg_hrcrx_max_byt'] = df['avg_hrcrx_max_byt'].fillna(0)

        # create n array from dataframe
        tmp_series = list(df.values.flatten())
        tmp_default_series = tmp_series[1::2]

        # calculate values needed to train on based on weeks
        tmp_training_count = self.default_num_train_weeks * self.default_stride_length
        start_training_data_index = len(tmp_default_series)-tmp_training_count
        end_training_data_index = len(tmp_default_series) - self.default_stride_length
        self.default_series = tmp_default_series[start_training_data_index:end_training_data_index]

        # call triple_exponential_smoothing with series = byte counts column in dataframe
        smooth_series = self.triple_exponential_smoothing(self.default_series, self.default_stride_length,
                                                          self.default_alpha, self.default_beta, self.default_gamma,
                                                          self.default_num_predictions)
        combined_data = np.append(self.default_series, smooth_series)

        # generate N new new sequential timestamps (per 15 min)
        start_date = df[''][end_training_data_index]
        result_datetimes = pd.date_range(start_date, periods=len(smooth_series), freq='15min')[0:]

        # assign new timestamps to datapoints
        nparray_data = np.array([result_datetimes, smooth_series]).transpose()

        # pass back completed dataframe or generate new csv file.
        return nparray_data

    def get_data_column_name(self):
        return self.data_column_name
