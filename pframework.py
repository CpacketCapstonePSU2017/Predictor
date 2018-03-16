"""
    This code is released under an MIT license

This class serves as a wrapper for PFramework and a model selector.
When adding a new model, it should follow a structure:
PModules                root folder for all models
    |
    model_name          folder dedicated to a model
        |
        model_name      model_name.py file
            |
            model_name  model_name class

    Every model should have:
    - A constructor that defines a default parameters passed
    - set_parameters() function prompting user to change parameters (if needed)
    - call_model() function doing all of the prediction. Should return nparray
"""
import pandas as pd
from predictor_resources.config import models, RESOURCES_DIR, Stride
from predictor_resources import db_config
from pydoc import locate
import sys
from os import path, remove
from root import ROOT_DIR
sys.path.append(path.join(ROOT_DIR,'CPacket-Common-Modules'))
from io_framework.csv_writer import CsvWriter
from PModules.ErrorAnalysis import ErrorAnalysis

class TrafficPredictor:
    _default_stride = None
    _num_of_series = None
    _selected_model = None
    _data_writer = None

    def __init__(self, database="predicted_data"):
        self._default_stride = Stride.WEEKLY
        self._num_of_series = 8
        self._selected_model = None
        self._data_writer = CsvWriter(host=db_config.host, port=db_config.port, username=db_config.username,
                                 password=db_config.password, database=database)

    def main(self):
        print("Welcome to the Traffic Predictor!")
        print("Please choose your model (enter its index):")
        for model in models:
            x = models.index(model)
            print("{0}: {1}".format(x, model))
        print("-: Exit")

        selection = input("Prompt: ")

        if selection == '-':
            return
        else:
            try:
                model = models[int(selection)]
                print("Please, wait...")
                np = self.call_model(model)
                df = self.nparray_to_dataframe(np)
                print("Finished prediction")
                print("Would you like to run Error analysis on the predicted data? [y]/[n]")
                selection = input("Prompt: ")
                if selection.lower() == 'y':
                    err_analysis = ErrorAnalysis(np)
                    err_analysis.compute_error()
                print("Would you like to write predicted data to database? [y]/[n]"
                      "\nIf selected [n] the data will be written to local csv file")
                selection = input("Prompt: ")
                if selection.lower() == 'y':
                    self.write_data_to_database(model, df)
                else:
                    self.write_data_to_csv(model, df)

            except IndexError:
                print("There's no model under index: {}".format(selection))
            except TypeError:
                print("ERROR: The model import failed. Please make sure to properly add/choose your model.")
                raise TypeError

    def call_model(self, model_name):
        model_root = 'PModules.' + model_name + "." + model_name + "." + model_name
        model = locate(model_root)
        self._selected_model = model()
        # Your model class instance
        self._selected_model.set_parameters()
        result = self._selected_model.call_model()

        return result

    def write_data_to_csv(self, model_name, df):
        if not isinstance(df, pd.DataFrame):
            print("Error reading the data from database. Please test this query in Chronograf/Grafana.")
        df.to_csv(path.join(RESOURCES_DIR, model_name + "_predicted.csv"))

    def write_data_to_database(self, model_name, df):
        df.to_csv(path.join(RESOURCES_DIR, model_name + "_predicted.csv"))
        self._data_writer.csv_file_to_db(measurement_to_use=model_name + '_predicted',
                                         new_csv_file_name=path.join(RESOURCES_DIR, model_name + "_predicted.csv"))
        remove(path.join(RESOURCES_DIR, model_name + "_predicted.csv"))

    def nparray_to_dataframe(self, nparray_data):
        indexes = pd.DataFrame(nparray_data[:, 0])
        indexes[0] = pd.to_datetime(indexes[0], format='%Y-%m-%d %H:%M:%S')
        cols = [self._selected_model.get_data_column_name()]
        df = pd.DataFrame(data=nparray_data[0:, 1:],
                          index=indexes[0],
                          columns=cols)
        return df


