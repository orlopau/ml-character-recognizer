from tensorflow import keras
import image_retriever

generators = image_retriever.retrieve_images('../imgs/')

model = keras.models.Sequential([
    keras.layers.Conv2D(64, kernel_size=3, activation='relu', input_shape=(28, 28, 1)),
    keras.layers.Flatten(),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(26, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit_generator(generator=generators['train'],
                    validation_data=generators['validation'],
                    epochs=100)

