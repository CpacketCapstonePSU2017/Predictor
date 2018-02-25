import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from predictor_resources.config import RESOURCES_DIR
import os
from io_framework.csv_writer import CsvWriter

def split_to_train_test(df):
    """
    Split data to train and test so that test data is always 1 week long
    :param df:
    :return:
    """
    size = len(df)
    test_size = 672/size
    if test_size > 1:
        print("The data should be more than 1 week ")
        raise ValueError
    train, test = train_test_split(df, test_size=test_size)
    return train, test

def normalize_train_data(df, sequence_length=3):
    """
    Normalization via dividing each value in the window by the first
    value of the window and then subtracting one.i.e [4,3,2] into [0, -0.25, -0.5]
    source: https://github.com/llSourcell/ethereum_future
    :param df: dataframe
    :param sequence_length: essentially a window size
    :return:
    """
    data = df['avg_hrcrx_max_byt'].fillna(0).values.tolist()
    # Convert the data to a 3D array (a x b x c)
    # Where a is the number of days, b is the window size, and c is the number of features in the data file
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])

    #Normalizing data by going through each window
    #Every value in the window is divided by the first value in the window, and then 1 is subtracted
    d0 = np.array(result)
    dr = np.zeros_like(d0)
    dr[:,1:,:] = d0[:,1:,:] / d0[:,0:1,:] - 1

    return dr

def normalization_minMaxScaler(df):
    """
    Normalize and denormalize data by uising minMaxScaler
    :param df:
    :return:
    """
    values = df['avg_hrcrx_max_byt'].fillna(0)
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(values.reshape(-1,1))
    rescaled_data = scaler.inverse_transform(scaled_data)
    return pd.DataFrame(scaled_data), pd.DataFrame(rescaled_data)

def denormalize_train_data (df):
    """
    Roll back the data to a regular scale
    :param df:
    :return:
    """
    df[:, 1:, :] = df[:, 1:, :] * df[:, 0:1, :] + 1
    return df

def shuffle(df):
    """
    Shuffle the train data
    :param df:
    :return:
    """

    return np.random.shuffle(df)


filepath = os.path.join(RESOURCES_DIR,"AccessPoint#3(Aruba3)Outgoing.csv")
writer = CsvWriter(host="", port=8888, username="", password="", database="")
raw_data = writer.csv_file_to_dataframe(new_filepath=filepath)
df, dr = normalization_minMaxScaler(raw_data)
train, test = split_to_train_test(raw_data)
dd = normalize_train_data(raw_data)
