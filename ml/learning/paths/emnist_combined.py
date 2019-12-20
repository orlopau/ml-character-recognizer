from learning.emnist.emnist import read_emnist_data
from learning.models import v1
import pandas as pd
from pathlib import Path
import data_util.transformations as trans
import matplotlib.pyplot as plt
import numpy as np


def append_arrays(x, y, ration=2):
    return np.append(x, y[:len(x) * ration], axis=0)


if __name__ == "__main__":
    path = Path(__file__).parent.absolute().parents[2] / 'datasets' / 'real' / 'dataset.csv'

    df = pd.read_csv(path)

    (x_train_p, y_train_p, x_test_p, y_test_p) = trans.pandas_df_to_2d(df)

    # show sample path image
    plt.imshow(x_train_p[0], cmap='gray_r')
    plt.show()

    (x_train_emnist, y_train_emnist, x_test_emnist, y_test_emnist) = read_emnist_data()

    x_train = append_arrays(x_train_p, x_train_emnist)
    y_train = append_arrays(y_train_p, y_train_emnist)

    v1.learn(x_train, y_train, x_test_p, y_test_p, epochs=15, name='emnist_combined')
