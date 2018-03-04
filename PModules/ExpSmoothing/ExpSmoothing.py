import numpy as np
import pandas as pd
#import matplotlib.pyplot
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
    def __init__(self, alpha=0.2, csv_filename=os.path.join(RESOURCES_DIR,'access_Point_1_incoming.csv')):
        """
        The parameters for this function are:
        :param series: The series passed in from call model.
        :param alpha: The alpha for N.
        :param csv_filename: The name of the CSV file with the series data.
        """
        self.default_alpha = alpha
        self.default_csv_filename = os.path.join(RESOURCES_DIR, csv_filename)
        self.data_column_name = None

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
        writer = CsvWriter(host=db_config.host, port=db_config.port, username=db_config.username,
                                 password=db_config.password, database='predicted_data')
        df = writer.csv_file_to_dataframe(new_filepath=self.default_csv_filename)
        series = list(df.values.flatten())
        bytcts = series[1::2]
        self.default_series = bytcts  # call triple_exponential_smoothing with series = byte counts column in dataframe
        smooth_series = self.exponential_smoothing(self.default_series, self.default_alpha)
        result_datetimes = pd.date_range(series[-2], periods=674, freq='15min')[1:]
        nparray_data = np.array([result_datetimes, smooth_series]).transpose()
        self.data_column_name = df.columns[1]
        return nparray_data

    def get_data_column_name(self):
        return self.data_column_name