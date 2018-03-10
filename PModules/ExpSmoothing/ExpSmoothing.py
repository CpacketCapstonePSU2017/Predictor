import numpy as np
import pandas as pd
from predictor_resources.config import RESOURCES_DIR
from predictor_resources import db_config
import os
import math
import sys
from os import path
from root import ROOT_DIR
sys.path.append(path.join(ROOT_DIR,'CPacket-Common-Modules'))
from io_framework.csv_writer import CsvWriter


class ExpSmoothing:
    def __init__(self, alpha=0.2, csv_filename=os.path.join(RESOURCES_DIR,'access_Point_1_incoming.csv'),
                 rows_to_use=None, error_array=0):
        """
        The parameters for this function are:
        :param series: The series passed in from call model.
        :param alpha: The alpha for N.
        :param csv_filename: The name of the CSV file with the series data.
        :param rows_to_use: This parameter is the number of 15 minutes intervals wanted used
        :param error_array: This is a flag that checks if you want a forecasted and actual value return along
                            with the timestamps in the numpy array.
        """
        self.default_alpha = alpha
        self.default_csv_filename = os.path.join(RESOURCES_DIR, csv_filename)
        self.data_column_name = None
        self.default_rtu = rows_to_use
        self.error_array = error_array

    def set_parameters(self):
        """
        Asking user to change a parameters specific to a model, if needed
        :return:
        """
        print("The default alpha: {}".format(self.default_alpha))
        print("Would you like to set the parameters for Exponential Smoothing first? [y]/[n]")
        selection = input("Prompt: ")
        if selection.lower() == 'y':
            print("Choose the alpha.")
            selection = input("Prompt: ")
            self.default_alpha = int(selection)

    def gen_weights(self, alpha, number_of_weights):
        """
        The parameters for a function that generates weights:
        :param alpha: The alpha for N.
        :param number_of_weights: The amount of weeks observed in the data.
        :return: A list the size of number_of_weights with weights from alpha that approach 0.
        """
        ws = list()
        if alpha >= 1:

            for i in range(0, number_of_weights-1):
                w = 0
                ws.append(w)
            w = alpha
            ws.append(w)
        else:
            for i in range(number_of_weights):
                w = alpha * ((1 - alpha) ** i)
                ws.append(w)
        return ws

    def exponential_smoothing(self, series, alpha):
        """
        The parameters to make an exponential smoothing prediction
        :param series: This is the series that is passed in from main that has the data to be processed.
        :param alpha: The starting weight.
        :return:
        """
        result = [series[0]]
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
        #This function returns a numpy array of timestamps and forecasted data, it call also return observed values
        if self.error_array is 0:
            writer = CsvWriter(host=db_config.host, port=db_config.port, username=db_config.username,
                               password=db_config.password, database='predicted_data')
            df = writer.csv_file_to_dataframe(new_filepath=self.default_csv_filename, usecols=[0, 1])
            series = list(df.values.flatten())
            bytcts = series[1::2]
            self.default_series = bytcts
            smooth_series = self.exponential_smoothing(self.default_series, self.default_alpha)
            result_datetimes = pd.date_range(series[-2], periods=674, freq='15min')[1:]
            nparray_data = np.array([result_datetimes, smooth_series]).transpose()
            self.data_column_name = df.columns[1]
            return nparray_data
        else:
            writer = CsvWriter(host=db_config.host, port=db_config.port, username=db_config.username,
                               password=db_config.password, database='predicted_data')
            row_end = self.default_rtu + 672
            df = writer.csv_file_to_dataframe(new_filepath=self.default_csv_filename, new_row_end=row_end, usecols=[0, 1])
            series = list(df.values.flatten())
            observed_val = series[-1345::2]
            if len(observed_val) < 673:
                return 0
            bytcts = series[1::2][:self.default_rtu]
            self.default_series = bytcts
            smooth_series = self.exponential_smoothing(self.default_series, self.default_alpha)
            result_datetimes = pd.date_range(series[-2], periods=674, freq='15min')[1:]
            nparray_data = np.array([result_datetimes, smooth_series, observed_val]).transpose()
            self.data_column_name = df.columns[1]
            return nparray_data

    def get_data_column_name(self):
        return self.data_column_name

#test = ExpSmoothing(error_array=0)
#print(test.call_model())
#test_too = ExpSmoothing(rows_to_use=28225, error_array=1)
#print(test_too.call_model())
