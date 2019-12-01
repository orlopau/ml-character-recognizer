import tensorflow as tf


# actual learning process

def learn(x_train, y_train, x_test, y_test, epochs=12, name='model'):
    batch_size = 128
    num_classes = 26

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
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))

    model.compile(loss=tf.keras.losses.categorical_crossentropy,
                  optimizer=tf.keras.optimizers.Adam(),
                  metrics=['accuracy'])

    print(model.summary())

    print("Training on " + str(len(x_train)) + " samples.")
    print("Validating with " + str(len(x_test)) + " samples.")

    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(x_test, y_test),
              shuffle=True)

    score = model.evaluate(x_test, y_test, verbose=0)

    print("Saving weights...")
    model.save("./" + name + ".h5")

    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    # save model as tflite file

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    open("./" + name + ".tflite", "wb").write(tflite_model)
