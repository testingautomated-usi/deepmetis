from os import makedirs
from os.path import exists, basename
from shutil import copyfile
import matplotlib


#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from tensorflow import keras
from properties import MODELS, IMG_SIZE, RESULTS_PATH
import numpy as np

# load the MNIST dataset
mnist = keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()


def input_reshape(x):
    # shape numpy vectors
    if keras.backend.image_data_format() == 'channels_first':
        x_reshape = x.reshape(x.shape[0], 1, 28, 28)
    else:
        x_reshape = x.reshape(x.shape[0], 28, 28, 1)
    x_reshape = x_reshape.astype('float32')
    x_reshape /= 255.0

    return x_reshape


def get_distance(v1, v2):
    return np.linalg.norm(v1 - v2)



def print_archive(archive):
    path = RESULTS_PATH + '/archive'
    dst = path + '/'
    if not exists(dst):
        makedirs(dst)
    for i, ind in enumerate(archive):
        filename = dst + basename(
            'archived_' + str(i) + '_label_' + str(ind.member.expected_label) + '_seed_' + str(ind.seed))
        plt.imsave(filename, ind.member.purified.reshape(28, 28), cmap=cm.gray, format='png')
        np.save(filename, ind.member.purified)
        assert (np.array_equal(ind.member.purified, np.load(filename + '.npy')))


# Useful function that shapes the input in the format accepted by the ML model.
def reshape(v):
    v = (np.expand_dims(v, 0))
    # Shape numpy vectors
    if keras.backend.image_data_format() == 'channels_first':
        v = v.reshape(v.shape[0], 1, IMG_SIZE, IMG_SIZE)
    else:
        v = v.reshape(v.shape[0], IMG_SIZE, IMG_SIZE, 1)
    v = v.astype('float32')
    v = v / 255.0
    return v
