import pandas
import numpy as np
from learning.models import v1

df = pandas.read_csv('dataset.csv').astype('float32')
df = df.sample(frac=1).reset_index(drop=True)

X = df.drop(df.columns[0], axis=1)
y = df['0']

data = X.to_numpy().reshape((len(X)), 28, 28)

validation_split = 0.75
validation_index = int(round(len(data) * validation_split))

v1.learn(data[:validation_index], y[:validation_index], data[validation_index:], y[validation_index:], epochs=3)
