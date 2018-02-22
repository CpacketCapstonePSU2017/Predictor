import numpy as np
from sklearn.model_selection import train_test_split


def split_to_train_test(df):
    """
    Split data to train and test so that test data is always 1 week long
    :param df:
    :return:
    """
    size = len(df)
    test_size = 672/size
    train, test = train_test_split(df, test_size=test_size)
    return train, test

def normalize_train_data(df, sequence_length):
    """
    Normalization via dividing each value in the window by the first
    value of the window and then subtracting one.i.e [4,3,2] into [0, -0.25, -0.5]
    source: https://github.com/llSourcell/ethereum_future
    :param df: dataframe
    :param sequence_length: essentially a window size
    :return:
    """
    data = df.tolist()
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

def shuffle(df):
    """
    Shuffle the train data
    :param df:
    :return:
    """

    return np.random.shuffle(df)

