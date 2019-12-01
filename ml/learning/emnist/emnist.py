import tensorflow as tf
from mlxtend.data import loadlocal_mnist
import matplotlib.pyplot as plt
import numpy as np

path = "../../../data/emnist"
print("Path for EMNIST data is " + path)

x_train, y_train = loadlocal_mnist(images_path=path + "/train-images-ubyte", labels_path=path + "/train-labels-ubyte")
x_test, y_test = loadlocal_mnist(images_path=path + "/test-images-ubyte", labels_path=path + "/test-labels-ubyte")

x_train = x_train.reshape((len(x_train), 28, 28), order='F') / 255.0
x_test = x_test.reshape((len(x_test), 28, 28), order='F') / 255.0


def reducer(x):
    return x - 1


# reduce every label by 1, because labels dont start at 0
y_train = reducer(y_train)
y_test = reducer(y_test)

plt.imshow(x_train[14], cmap='gray_r')
plt.show()

print("Should show a " + str(y_train[14]))

# actual learning process

batch_size = 128
num_classes = 26
epochs = 12

x_train = tf.expand_dims(x_train, 3)
x_test = tf.expand_dims(x_test, 3)

y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_test = tf.keras.utils.to_categorical(y_test, num_classes)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(32, kernel_size=(3, 3),
                                 activation='relu',
                                 input_shape=(28, 28, 1)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Dropout(0.25))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))

model.compile(loss=tf.keras.losses.categorical_crossentropy,
              optimizer=tf.keras.optimizers.Adam(),
              metrics=['accuracy'])

print(model.summary())

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test),
          shuffle=True)

score = model.evaluate(x_test, y_test, verbose=0)

print("Saving weights...")
model.save('./emnist_cnn.h5')

print('Test loss:', score[0])
print('Test accuracy:', score[1])
