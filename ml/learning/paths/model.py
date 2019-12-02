from learning.models import v1
import pandas as pd
import numpy as np
import os
from pathlib import Path
import data_util.transformations as trans
import matplotlib.pyplot as plt

path = Path(__file__).parent.absolute().parents[2] / 'datasets' / 'real' / 'dataset.csv'

df = pd.read_csv(path)

(x_train, y_train, x_test, y_test) = trans.pandas_df_to_2d(df)

plt.imshow(x_train[0], cmap='gray_r')
plt.show()


v1.learn(x_train, y_train, x_test, y_test, epochs=12)
