import numpy as np


# converts a pandas df consisting of rows with columns: char, pixel0, pixel1, pixel2, ... , pixel28*28
def pandas_df_to_2d(df, validation_split=0.75, scale_divisor=255.):
    np.random.shuffle(df.values)

    x = df.drop(df.columns[0], axis=1)
    y = df['0']

    data = x.to_numpy().reshape((len(x)), 28, 28) / scale_divisor
    y = y.to_numpy()

    validation_index = int(round(len(data) * validation_split))

    return (
        data[:validation_index],
        y[:validation_index],
        data[validation_index:],
        y[validation_index:]
    )
