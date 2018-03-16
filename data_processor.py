"""
    This code is released under an MIT license

This script works with getting the data to or from InfluxDB.

     - You can send your own data, if you have a .csv file. It will go
       Through the process of filling the data gaps.
     - You can get the data from InfluxDB in form of .csv file.
       The default database is 'AccessPoints'.
     - The files are stored/used from 'predictor_resources' folder.
"""
from predictor_resources.config import RESOURCES_DIR
from predictor_resources import db_config
import sys
from os import path, remove
from root import ROOT_DIR
sys.path.append(path.join(ROOT_DIR,'CPacket-Common-Modules'))
from io_framework.csv_writer import CsvWriter
from io_framework.db_connector.db_connector import InfluxDBConnector
from io_framework.csv_fill_data_gaps import fill_data_gaps

database = 'AccessPoints'  # choose this if you want to use different DB
data_processor = CsvWriter(host=db_config.host, port=db_config.port, username=db_config.username,
                                 password=db_config.password, database=database)
connector = InfluxDBConnector(host=db_config.host, port=db_config.port, database=database)

def data_with_filled_gaps_to_db(file_path=None, new_measurement=None):
    df = data_processor.csv_file_to_dataframe(new_filepath=file_path)  # Change usecols here if you need
    dr = fill_data_gaps(init_data=df)
    dr.set_index('', inplace=True)
    dr.to_csv(path_or_buf=path.join(RESOURCES_DIR,"temp.csv"))
    data_processor.csv_file_to_db(measurement_to_use=new_measurement, new_csv_file_name=path.join(RESOURCES_DIR,"temp.csv"))
    remove(path.join(RESOURCES_DIR,"temp.csv"))


print("Welcome! Use this script to push/pull data using InfluxDB")
print("You need to have data on local .csv files since each model uses csv file for prediction")
print("Right now the database used: {}".format(database))

print("What do you want to do?")
print("1 - Push more data to: {}".format(database))
print("2 - Grab the data from: {}".format(database))
selection = input("Prompt: ")

if selection == '1':
    print("\t\t\t********WARNING********")
    print("IO framework is reading first and second column by default, timestamp and bytecount respectivelly.")
    print("If you have values you want to store in a different column, make sure to change default value of 'usecols' parameter")
    print("Type file name (should reside in 'predictor resources' folder)")
    selection = input("Prompt: ")
    file_path = path.join(RESOURCES_DIR,selection+".csv")
    print("Type name of measurement to be created")
    selection = input("Prompt: ")
    measurement = selection
    data_with_filled_gaps_to_db(new_measurement=measurement, file_path=file_path)
    print("Data successfully stored in {}".format(database + "." + measurement))
elif selection == '2':
    print("Choose the measurement to use (by index):")
    measure_list = connector.list_measurements()
    for measure in measure_list:
        x = measure_list.index(measure)
        print("{}: {}".format(x,measure['name']))

    measurement_index = int(input("Prompt: "))
    measurement = measure_list[measurement_index]['name']
    file_path = path.join(RESOURCES_DIR, measurement + ".csv")
    print("Please, wait...")
    data_processor.data_to_csv_file(db_query='SELECT * FROM ' + measurement, measurement_to_use=measurement, new_csv_file_name=file_path)
    print("Data successfully stored in {}".format(file_path))

