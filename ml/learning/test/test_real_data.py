import tensorflow as tf
from learning import image_retriever
import matplotlib.pyplot as plt
import numpy as np
import string

path_to_tflite = "../emnist/emnist_cnn.tflite"

interpreter = tf.lite.Interpreter(model_path=path_to_tflite)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test model with data from android paths
generators = image_retriever.retrieve_images('../../imgs/')
# use train generator, doesnt really matter, actually just gets images in a valid format
trainer = generators['validation']

input_shape = input_details[0]['shape']

correct_predictions = np.zeros(26)
wrong_predictions = np.zeros(26)

batch_index = 0
number_of_test_batches = 200

for batch in trainer:

    batch_index += 1

    if batch_index > number_of_test_batches:
        break

    print("Batch number " + str(batch_index))

    data = batch[0]
    labels = batch[1]

    # iterate over batch
    for i in range(0, len(data)):
        img = data[i]
        input_data = np.array([img])

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        predicted = output_data[0].argmax()
        actual = labels[i].argmax()

        if predicted == actual:
            correct_predictions[actual] += 1
        else:
            wrong_predictions[actual] += 1

print("Correctly predicted: " + str(correct_predictions.sum()))
print("Wrongly predicted: " + str(wrong_predictions.sum()))

accuracy = correct_predictions.sum() / (correct_predictions.sum() + wrong_predictions.sum())

print("Accuracy: " + str(accuracy))

# create plot
fig, ax = plt.subplots()
index = np.arange(correct_predictions.size)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, list(correct_predictions), bar_width,
                 alpha=opacity,
                 color='g',
                 label='Correct')

rects2 = plt.bar(index + bar_width, list(wrong_predictions), bar_width,
                 alpha=opacity,
                 color='r',
                 label='Wrong')

plt.xlabel('Predictions')
plt.ylabel('Number')
plt.title('Predictions in model')
plt.xticks(index + bar_width, list(string.ascii_uppercase))
plt.legend()

plt.tight_layout()
plt.show()
