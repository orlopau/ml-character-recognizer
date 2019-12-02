from mlxtend.data import loadlocal_mnist
from learning.models import v1

path = "../../../datasets/emnist"
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

# actual learning process

v1.learn(x_train, y_train, x_test, y_test, name='emnist')
