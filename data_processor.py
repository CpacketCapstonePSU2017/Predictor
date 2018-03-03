from predictor_resources.config import RESOURCES_DIR
from predictor_resources import db_config
import sys
from os import path
from root import ROOT_DIR
sys.path.append(path.join(ROOT_DIR,'CPacket-Common-Modules'))
from io_framework.csv_writer import CsvWriter

database = 'AccessPoints'
data_processor = CsvWriter(host=db_config.host, port=db_config.port, username=db_config.username,
                                 password=db_config.password, database=database)
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
    data_processor.csv_file_to_db(measurement_to_use=measurement, new_csv_file_name=selection)
    print("Data successfully stored in {}".format(database + "." + measurement))
elif selection == '2':
    print("Choose the measurement to use:")
    print("PRINT LIST OF MEASUREMENT FROM DATABASE")
    measurement = 'access_Point_1_incoming'
    file_path = path.join(RESOURCES_DIR, measurement + ".csv")
    data_processor.data_to_csv_file(db_query='SELECT * FROM ' + measurement, measurement_to_use=measurement, new_csv_file_name=file_path)
    print("Data successfully stored in {}".format(file_path))
