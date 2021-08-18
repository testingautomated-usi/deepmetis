import os
import csv
import glob
import h5py
import argparse
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from utils import properties
from tensorflow.keras.datasets import mnist
from tensorflow.keras import backend as K
from stats import is_diff_sts

os.environ['KMP_DUPLICATE_LIB_OK']='True'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--augment", "-augment", default='yes',
                        type=str, help="Augment test suite or not")

    args = parser.parse_args()

    augmentation = args.augment

    operators = ['add_weights_regularisation']
    index = 0
    for mutation_prefix in ('mnist_add_weights_regularisation_mutated0_MP_l1_l2_0_',):
        #tools = ['dm', 'dm', 'df', 'df', 'dj', 'dj']
        tools = ['dm']
        input_locs = ['../DeepMetis-MNIST/']
        model_dir = '../DeepMetis-MNIST/models/'

        weak_ts_dir = 'mnist_weak.h5'
        ((x_train, y_train), (x_test, y_test)) = mnist.load_data()

        hf = h5py.File(weak_ts_dir, 'r')
        x_test = np.asarray(hf.get('x_test'))
        y_test = np.asarray(hf.get('y_test'))
        (img_rows, img_cols) = (28, 28)
        num_classes = 10

        if (K.image_data_format() == 'channels_first'):
            x_test_new = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
            input_shape = (1, img_rows, img_cols)
        else:
            x_test_new = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
            input_shape = (img_rows, img_cols, 1)

        x_test_new = x_test_new.astype('float32')
        x_test_new /= 255
        y_test_new = y_test

        run = 0
        for input_loc in input_locs:
            output_file = input_loc + "/output.csv"

            if os.path.exists(output_file):
                os.remove(output_file)

            #print("output_file:" + str(output_file))
            with open(output_file, 'a') as f1:
                writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
                writer.writerow([str("Run Num"), str("Input Num"), str("WLX Killed"), str("WLX p-value"), str("Effect Size")])

            file_num = 0

            for filename in glob.glob((input_loc + '/results_mnist_add_weights_regularisation_mutated0_MP_l1_l2_0_1*')):   
                if not '.csv' in filename:
                    #priority_inputs = np.load(filename + "/prioritised.npy")
                    file_num = file_num + 1
                    if tools[run] == 'dm' or tools[run] == 'dj':
                        image_dir = str(filename) + "/results/archive/*"
                    else:
                        image_dir = str(filename) + "/results/*"

                    orig_accuracy_file = filename + "/orig_accuracy.csv"
                    mutant_accuracy_file = filename + "/mutant_accuracy.csv"
                    y_test_ann = y_test_new
                    x_test_ann = x_test_new
                    input_num = 0
                    if augmentation == 'yes':
                        for image in glob.glob(image_dir):
                            if '.npy' in image:
                                input_num = input_num + 1
                                if tools[run] == 'dm' or tools[run] == 'df':
                                    startIndex = (image.index('_label_', 0, len(image)) + len('_label_'))
                                else:
                                    startIndex = (image.index('_l_', 0, len(image)) + len('_l_'))
                                label = int(image[startIndex:startIndex + 1])
                                y_test_ann = np.append(y_test_ann, label)
                                x_test_ann = np.append(x_test_ann, np.load(image, allow_pickle=True), axis=0)

                    y_test_ann = keras.utils.to_categorical(y_test_ann, num_classes)
                    print("new:" + str(y_test_ann.shape))

                    original_accuracies = []
                    mutant_accuracies = []
                    for i in range(0, 20):
                        graph1 = tf.Graph()
                        with graph1.as_default():
                            session1 = tf.compat.v1.Session()
                            with session1.as_default():
                                original_model_location = model_dir + 'mnist_original_' + str(i) + ".h5"
                                #print(original_model_location)
                                original_model =  tf.keras.models.load_model(original_model_location)
                                score_orig = original_model.evaluate(x_test_ann, y_test_ann, verbose=0)
                                #print("Orig:" + str(score_orig))
                                original_accuracies.append(score_orig[1])
                                with open(orig_accuracy_file, 'a') as f1:
                                    writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
                                    writer.writerow([str(i), str(score_orig[1])])

                                mutant_model_location = model_dir + mutation_prefix + str(i) + ".h5"
                                #print(mutant_model_location)
                                mutant_model = tf.keras.models.load_model(mutant_model_location)
                                score_mutant = mutant_model.evaluate(x_test_ann, y_test_ann, verbose=0)
                                #print("Mutant:" + str(score_mutant))
                                mutant_accuracies.append(score_mutant[1])

                                with open(mutant_accuracy_file, 'a') as f1:
                                    writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
                                    writer.writerow([str(i), str(score_mutant[1])])

                    properties.statistical_test = 'WLX'
                    wlx_is_sts, wlx_p_value, wlx_effect_size = is_diff_sts(original_accuracies, mutant_accuracies)
                    print('Mutant Killed:', wlx_is_sts)

                    with open(output_file, 'a') as f1:
                        writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
                        writer.writerow([str(filename), str(input_num), str(wlx_is_sts), str(wlx_p_value), str(wlx_effect_size)])

        run = run + 1
        index = index + 1
