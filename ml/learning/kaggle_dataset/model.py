import pandas
from learning.models import v1

df = pandas.read_csv('../../../datasets/kaggle/dataset.csv').astype('float32')
df = df.sample(frac=1).reset_index(drop=True)

X = df.drop(df.columns[0], axis=1)
y = df['0']

data = X.to_numpy().reshape((len(X)), 28, 28) / 255.

validation_split = 0.75
validation_index = int(round(len(data) * validation_split))

print("Should show a " + str(y[14]))

v1.learn(data[:validation_index], y[:validation_index], data[validation_index:], y[validation_index:], epochs=3, name='kaggle_A_to_Z')
