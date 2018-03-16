"""
    This code is released under an MIT license
"""
import numpy as np
import pandas as pd
from sklearn import metrics
from matplotlib import pyplot
np.set_printoptions(threshold=np.nan)

import root
import sys
from os import path
from predictor_resources.config import RESOURCES_DIR
sys.path.append(path.join(root.ROOT_DIR, 'CPacket-Common-Modules'))
from io_framework.csv_writer import CsvWriter


class ErrorAnalysis:

    def __init__(self, predicted, data_file="access_Point_1_incoming.csv"):
        self.csvWriter = CsvWriter(host="", port=0, username="", password="", database="", new_measurement="",
                                   new_cvs_file_name="")
        self.predictedValues = predicted
        self.actualValues = self.csvWriter.csv_file_to_dataframe_date_selection(path.join(RESOURCES_DIR, data_file), pd.Timestamp(predicted[0, 0]), pd.Timestamp(predicted[-1, 0]))
    def compute_error(self):
        actual = self.actualValues["avg_hrcrx_max_byt"].tolist()
        predicted = self.predictedValues[:, 1].tolist()
        count = 0

        self.meanSquaredError = metrics.mean_squared_error(actual, predicted)
        self.meanAbsoluteError = metrics.mean_absolute_error(actual, predicted)

        print("Mean Squared Error: " + str(self.meanSquaredError))
        print("Mean Absolute Error: " + str(self.meanAbsoluteError))

    def plot_predicted_vs_actual(self):
        pyplot.plot(self.predictedValues[:, 0], self.predictedValues[:, 1])
        pyplot.plot(np.array(self.actualValues[""].tolist()), np.array(self.actualValues["avg_hrcrx_max_byt"].tolist()))
        pyplot.legend(['Predicted Values', 'Actual Values'])
        pyplot.show()
