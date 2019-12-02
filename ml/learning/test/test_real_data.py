import tensorflow as tf
from learning import image_retriever
import matplotlib.pyplot as plt
import numpy as np
import string
import glob
import pandas
import data_util.transformations as trans


def test_tflite_model(path_to_tflite):
    interpreter = tf.lite.Interpreter(model_path=path_to_tflite)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    df = pandas.read_csv('../../../datasets/real/dataset.csv').astype('float32')

    input_shape = input_details[0]['shape']
    (x_train, y_train, x_test, y_test) = trans.pandas_df_to_2d(df, validation_split=1)

    correct_predictions = np.zeros(26)
    wrong_predictions = np.zeros(26)

    for i in range(0, len(x_train)):
        print(str(i) + " of " + str(len(x_train)))

        input_data = x_train[i]
        input_data = tf.expand_dims(input_data, 2)
        input_data = tf.expand_dims(input_data, 0)
        label = y_train[i]

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        predicted = output_data[0].argmax()

        if predicted == label:
            correct_predictions[int(label)] += 1
        else:
            wrong_predictions[int(label)] += 1

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
    plt.title(path_to_tflite.split('/')[-1] + "  " + str(round(accuracy, 2)) + "%")
    plt.xticks(index + bar_width, list(string.ascii_uppercase))
    plt.legend()

    plt.tight_layout()

    name = path_to_tflite.split('/')[-1].split('.')[0]
    plt.savefig('./doc/' + name + '.png')


if __name__ == '__main__':
    files = glob.glob('../**/*.tflite')
    for file in files:
        test_tflite_model(file)
