import tensorflow as tf
import pathlib
import numpy as np


def retrieve_images(path: str):
    p = pathlib.Path(path)
    image_nr = len(list(p.glob('**/*.png')))
    print("Found " + str(image_nr) + " images!")

    classes = np.array([item.name for item in p.glob('*')])
    print("Found " + str(len(classes)) + " classes!")

    image_generator = tf.keras.preprocessing.image.ImageDataGenerator(
        validation_split=0.2,
        rescale=1./255
    )

    train_generator = image_generator.flow_from_directory(
        directory=path,
        target_size=(28, 28),
        batch_size=20,
        shuffle=True,
        subset='training',
        color_mode='grayscale',
        class_mode='categorical')

    validation_generator = image_generator.flow_from_directory(
        directory=path,
        target_size=(28, 28),
        batch_size=20,
        shuffle=True,
        subset='validation',
        color_mode='grayscale',
        class_mode='categorical')

    return {
        'train': train_generator,
        'validation': validation_generator
    }
