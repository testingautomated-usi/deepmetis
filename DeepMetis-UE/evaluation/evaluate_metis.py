import csv
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import tensorflow as tf
import keras.backend as K
import gc
from tensorflow import math

from scipy.stats import wilcoxon

import append_solutions


def angle_loss_fn(y_true, y_pred):
    x_p = math.sin(y_pred[:, 0]) * math.cos(y_pred[:, 1])
    y_p = math.sin(y_pred[:, 0]) * math.sin(y_pred[:, 1])
    z_p = math.cos(y_pred[:, 0])

    x_t = math.sin(y_true[:, 0]) * math.cos(y_true[:, 1])
    y_t = math.sin(y_true[:, 0]) * math.sin(y_true[:, 1])
    z_t = math.cos(y_true[:, 0])

    norm_p = math.sqrt(x_p * x_p + y_p * y_p + z_p * z_p)
    norm_t = math.sqrt(x_t * x_t + y_t * y_t + z_t * z_t)

    dot_pt = x_p * x_t + y_p * y_t + z_p * z_t

    angle_value = dot_pt/(norm_p * norm_t)
    angle_value = tf.clip_by_value(angle_value, -0.99999, 0.99999)

    loss_val = (math.acos(angle_value))

    return tf.reduce_mean(loss_val, axis=-1)


#calculates cohen's kappa value
def cohen_d(orig_accuracy_list, accuracy_list):
    nx = len(orig_accuracy_list)
    ny = len(accuracy_list)
    dof = nx + ny - 2
    pooled_std = np.sqrt(((nx-1)*np.std(orig_accuracy_list, ddof=1) ** 2 + (ny-1)*np.std(accuracy_list, ddof=1) ** 2) / dof)
    result = (np.mean(orig_accuracy_list) - np.mean(accuracy_list)) / pooled_std
    return result


def is_diff_sts(orig_accuracy_list, accuracy_list, threshold = 0.05):

    w, p_value = wilcoxon(orig_accuracy_list, accuracy_list)

    effect_size = cohen_d(orig_accuracy_list, accuracy_list)

    if problem_type == 'regression':
        is_sts = ((p_value < threshold) and effect_size <= -0.5)
    else:
        is_sts = ((p_value < threshold) and effect_size >= 0.5)

    return is_sts, p_value, effect_size


def get_original_models():
    original_models = []
    for m in range(num_models):
        original_models.append(tf.keras.models.load_model(os.path.join(models_dir, original_model_name % m), custom_objects={'angle_loss_fn': angle_loss_fn}))
    return original_models

def get_mutated_modes(mutated_model_name):
    mutated_models = []
    for m in range(num_models):
        mutated_models.append(tf.keras.models.load_model(os.path.join(models_dir, mutated_model_name % m), custom_objects={'angle_loss_fn': angle_loss_fn}))
    return mutated_models


def run_original_ts_eval():
    otput_csv = os.path.join(outputs_dir, operator + '_orig.csv')
    output = []

    check_ds = os.path.join(datasets_dir, 'srch_img_10.npy')

    if os.path.isfile(check_ds):
        x_img_test = np.load(os.path.join(datasets_dir, 'srch_img_10.npy'))
        x_ha_test = np.load(os.path.join(datasets_dir, 'srch_ha_10.npy'))
        y_gaze_test = np.load(os.path.join(datasets_dir, 'srch_gaze_10.npy'))

        scores_orig = []
        scores_mut = []

        # print( x_img_test.shape)
        num_inp = x_img_test.shape[0] - x_init

        for m in range(num_models):
            score_orig = original_models[m].evaluate([x_img_test, x_ha_test], y_gaze_test, verbose=0)
            scores_orig.append(score_orig[1])

        for m in range(num_models):
            score_mut = mutated_models[m].evaluate([x_img_test, x_ha_test], y_gaze_test, verbose=0)
            scores_mut.append(score_mut[1])

        is_sts, p_value, effect_size = is_diff_sts(scores_orig, scores_mut)

        output.append([0, num_inp, operator, is_sts, p_value, effect_size])

        print("Mutant killed by the original test set?: " +  str(is_sts))

    else:
        print("Dataset does not exist")

    if output:
        with open(otput_csv, 'a') as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n', )
            writer.writerows(output)

        print("__________________")


def run_augm_ts_eval():
    otput_csv = os.path.join(outputs_dir, operator + '_mut.csv')
    output = []

    check_ds = os.path.join(datasets_dir, 'x_img_wts_' + operator + "_" + str(num_results-1) + '.npy')

    if os.path.isfile(check_ds):
        x_img_test = np.load(os.path.join(datasets_dir, 'x_img_wts_' + operator + "_" + str(num_results-1) + '.npy'))
        x_ha_test = np.load(os.path.join(datasets_dir, 'x_ha_wts_' + operator + "_" + str(num_results-1) + '.npy'))
        y_gaze_test = np.load(os.path.join(datasets_dir, 'y_gaze_wts_' + operator + "_" + str(num_results-1) + '.npy'))

        scores_orig = []
        scores_mut = []

        # print( x_img_test.shape)
        num_inp = x_img_test.shape[0] - x_init

        for m in range(num_models):
            score_orig = original_models[m].evaluate([x_img_test, x_ha_test], y_gaze_test, verbose=0)
            scores_orig.append(score_orig[1])

        for m in range(num_models):
            score_mut = mutated_models[m].evaluate([x_img_test, x_ha_test], y_gaze_test, verbose=0)
            scores_mut.append(score_mut[1])

        is_sts, p_value, effect_size = is_diff_sts(scores_orig, scores_mut)

        output.append([0, num_inp, operator, is_sts, p_value, effect_size])

        print("Mutant killed by the augmented test set?: " + str(is_sts))

    else:
        print("Dataset does not exist")

    if output:
        with open(otput_csv, 'w') as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n', )
            writer.writerows(output)

        print("__________________")


if __name__ == "__main__":

    problem_type = "regression" #classification
    models_dir = "models"
    original_model_name = 'lenet_original_%d.h5'
    datasets_dir = "datasets"
    outputs_dir = "output"
    operator = "AAL"

    operators_n_configs = {
        'LR': 'lenet_change_learning_rate_mutated0_MP_False_0.0037_%d.h5',
        'DT': 'lenet_delete_training_data_mutated0_MP_46.41_%d.h5',
        'AN': 'lenet_add_noise_mutated0_MP_84.38_%d.h5',
        'UN': 'lenet_unbalance_train_data_mutated0_MP_100_%d.h5',
        'CHE': 'lenet_change_epochs_mutated0_MP_False_32_%d.h5',
        'CWI': 'lenet_change_weights_initialisation_mutated0_MP_lecun_uniform_1_%d.h5',
        'AAL': 'lenet_add_activation_function_mutated0_MP_softsign_9_%d.h5',
        'CL': 'lenet_change_label_mutated0_MP_21.88_%d.h5',
        'AWR1': 'lenet_add_weights_regularisation_mutated0_MP_l2_1_%d.h5',
        'AWR3': 'lenet_add_weights_regularisation_mutated0_MP_l2_3_%d.h5',
    }

    num_results = 1
    num_models = 20

    x_img_test_init = np.load(os.path.join(datasets_dir, 'srch_img_10.npy'))
    x_init = x_img_test_init.shape[0]

    original_models = get_original_models()

    mo_model = operators_n_configs.get(operator)

    mutated_models = get_mutated_modes(mo_model)

    run_original_ts_eval()
    run_augm_ts_eval()
