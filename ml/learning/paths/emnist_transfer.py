import tensorflow as tf
from learning.models import v1 as model_gen
from learning.models import v1
import pandas as pd
from pathlib import Path
import data_util.transformations as trans
import matplotlib.pyplot as plt

if __name__ == "__main__":
    model = model_gen.load_model_from_h5("../emnist/emnist.h5")

    for layer in model.layers:
        layer.trainable = False

    model.layers[9].trainable = True
    model.layers[7].trainable = True

    model.compile(loss=tf.keras.losses.categorical_crossentropy,
                  optimizer=tf.keras.optimizers.Adam(),
                  metrics=['accuracy'])

    path = Path(__file__).parent.absolute().parents[2] / 'datasets' / 'real' / 'dataset.csv'

    df = pd.read_csv(path)

    (x_train, y_train, x_test, y_test) = trans.pandas_df_to_2d(df)

    plt.imshow(x_train[0], cmap='gray_r')
    plt.show()

    v1.learn(x_train, y_train, x_test, y_test, epochs=30, model=model, name='emnist_path_transfer')
