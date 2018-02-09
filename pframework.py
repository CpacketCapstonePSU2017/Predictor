"""
This class serves as a wrapper for PFramework and a model selector.
When adding a new model, it should follow a structure:
PModules                root folder for all models
    |
    model_name          folder dedicated to a model
        |
        model_name      model_name.py file
            |
            model_name  model_name class
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

class TrafficPredictor:
    _default_stride = Stride.WEEKLY
    _num_of_series = 8
    _selected_model = None
    _data_writer = CsvWriter(host=db_config.host, port=db_config.port, username=db_config.username,
                             password=db_config.password, database="predicted_data")

    def main(self):
        print("Welcome to the Traffic Predictor!")
        print("Would you like to set the parameters for predictor first? [y]/[n]")
        print("The default stride: {}".format(self._default_stride.name))
        print("The default number of  series: {}".format(self._num_of_series))
        selection = input("Prompt: ")
        if selection.lower() == 'y':
            print("Choose the stride (WEEKLY/DAILY): [W]/[D]")
            selection = input("Prompt: ")
            if selection.upper() == 'W':
                self._default_stride = Stride.WEEKLY
            if selection.upper() == 'D':
                self._default_stride = Stride.DAILY
            print("Choose the number of series.")
            selection = input("Prompt: ")
            if self._default_stride == Stride.DAILY and int(selection) < 7:
                print("You cannot use training set less than 7 days. It will be left as a default")
            if self._default_stride == Stride.WEEKLY and int(selection) > 52:
                print("The number of series cannot exceed one year. It will be left as a default")
            else:
                self._num_of_series = int(selection)
        print("Please choose your model (enter its index):")
        for model in models:
            x = models.index(model)
            print("{0}: {1}".format(x, model))
        print("-: Exit")

        selection = input("Prompt: ")

        for model in models:
            x = str(models.index(model))
            if selection == '-':
                return
            elif selection == x:
                try:
                    df = self.nparray_to_dataframe(self.call_model(model))
                    print("Would you like to write predicted data to database?"
                          "\nIf selected [n] the data will be written to local csv file")
                    selection = input("Prompt: ")
                    if selection.lower() == 'y':
                        self.write_data_to_database(model, df)
                    else:
                        self.write_data_to_csv(model, df)

                except TypeError:
                    print("ERROR: The model import failed. Please make sure to properly add your model.")
                    raise TypeError
            else:
                print("ERROR: there's no such model")

    def call_model(self, model_name):
        model_root = 'PModules.' + model_name + "." + model_name + "." + model_name
        model = locate(model_root)
        self._selected_model = model(default_stride=self._default_stride, window_length=self._num_of_series)
        # Your model class instance
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


# predictor = TrafficPredictor()
# predictor.main()
