"""
    This code is released under an MIT license
"""
import numpy as np
import pandas as pd
from scipy import signal
import root
import sys
from os import path
from predictor_resources.config import RESOURCES_DIR, Stride
sys.path.append(path.join(root.ROOT_DIR, 'CPacket-Common-Modules'))
from io_framework.csv_writer import CsvWriter


class SimpleMovingAverage:
    """
    Calculates the Simple Moving Average on a daily/weekly basis
     This class makes N different series depending on the selected stride, 96(4*24) in the case of daily and 672(4*24*7)
     in the case of weekly. This is under the assumption that there is a periodic relationship in the data. For example,
     for a daily stride, it is being assumed that there is a correlation between all the 9AM values that occur, and the
     prediction for the next 9AM value is a moving average of all the selected days before it.

    :param default_stride: represents the stride for calculating the moving average (DAILY/WEEKLY)
    :param window_length: Number of days in a single series
    :param data_file: Name of the file that exists in the predictor_resources folder
    :return: numpy array object with two columns, a timeseries object(in epoch format) and the predicted bytecount

    """

    formattedInput = []
    lastDate = ""
    data_column_name = ""

    def __init__(self, default_stride=Stride.WEEKLY, window_length=8, data_file="access_Point_1_incoming.csv"):
        self.defaultStride = default_stride
        self.windowLength = window_length
        self.csvWriter = CsvWriter(host="", port=0, username="", password="", database="", new_measurement="",
                                   new_cvs_file_name="")

        # Data returned as two columns. One with timeseries and other with bytecount values
        self.returned_data_frame = self.csvWriter.csv_file_to_dataframe(new_filepath=path.join(RESOURCES_DIR, data_file)
                                            ,new_row_start=0, new_row_end=self.defaultStride.value * self.windowLength)

    def set_parameters(self):
        """
        Asking user to change a parameters specific to a model, if needed
        :return:
        """
        print("The default stride: {}".format(self.defaultStride.name))
        print("The default number of  series: {}".format(self.windowLength))
        print("Would you like to set the parameters for Simple Moving Average first? [y]/[n]")
        selection = input("Prompt: ")
        if selection.lower() == 'y':
            print("Choose the stride (WEEKLY/DAILY): [W]/[D]")
            selection = input("Prompt: ")
            if selection.upper() == 'W':
                self.defaultStride = Stride.WEEKLY
            if selection.upper() == 'D':
                self.defaultStride = Stride.DAILY
            print("Choose the number of series.")
            selection = input("Prompt: ")
            if self.defaultStride == Stride.DAILY and int(selection) < 7:
                print("You cannot use training set less than 7 days. It will be left as a default")
            if self.defaultStride == Stride.WEEKLY and int(selection) > 52:
                print("The number of series cannot exceed one year. It will be left as a default")
            else:
                self.windowLength = int(selection)

    def initialize_dataframe_output(self):
        # Input formatting for future calculation
        numpy_array = np.array(self.returned_data_frame)[:, 1]
        numpy_array = numpy_array.reshape((numpy_array.size//self.defaultStride.value, self.defaultStride.value)).transpose()
        self.formattedInput = numpy_array

        # Getting the last day in the "training" data. Used to generate the output timeseries later
        self.lastDate = np.array(self.returned_data_frame)[-1:, :-1][0][0]

    def call_model(self):
        self.initialize_dataframe_output()
        numpy_array = self.formattedInput

        # makes a numpy array of length(windowLength) and divides each with the scalar value of window.length
        x = np.ones(self.windowLength)/self.windowLength

        if self.defaultStride == Stride.DAILY:
            loop_count = 7
        elif self.defaultStride == Stride.WEEKLY:
            loop_count = 1

        # Calculating moving average here
        for i in range(loop_count):
            y = signal.convolve(numpy_array, [x], mode="valid")
            numpy_array = np.concatenate((numpy_array, y), axis=1)
            numpy_array = numpy_array[:, 1:]

        if self.defaultStride == Stride.DAILY:
            predictions = numpy_array[:, -7:]
            predictions = predictions.transpose().reshape(1, predictions.size)[0]

        elif self.defaultStride == Stride.WEEKLY:
            predictions = numpy_array[:, -1]

        # Creates a numpy array(One week long), because the function is inclusive getting rid of the first element
        result_datetimes = pd.date_range(self.lastDate, periods=Stride.WEEKLY.value+1, freq='15min')[1:]
        nparray_data = np.array([result_datetimes, predictions]).transpose()
        self.data_column_name = self.returned_data_frame.columns[1]
        return nparray_data

    def get_data_column_name(self):
        return self.data_column_name

