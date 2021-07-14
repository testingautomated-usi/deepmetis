import glob
import os
import pandas as pd

if __name__ == '__main__':
    directory = "leave_one_out_RQ4/"
    abbreviation_dict = {'change_label': 'TCL (84.38\%)', 'make_output_classes_overlap': 'TCO (96.88\%)',
                         'unbalance_train_data': 'TUD (90.62\%)', 'change_learning_rate': 'HLR (0.064)',
                         'change_optimisation_function': 'OCH (\'rmsprop\')',
                         'remove_activation_function': 'ARM (l5)',  'change_weights_initialisation_ones_0': 'WCI (l0; \'ones\')',
                         'change_weights_initialisation_random_uniform_0': 'WCI (l0; \'random_uniform\')',
                         'add_weights_regularisation_l1_l2_0': 'RAW (l0; \'l1\_l2\')',
                         'add_weights_regularisation_l2_0': 'RAW (l0; \'l2\')',
                         'change_activation_function_hard_sigmoid_6': 'ACH (l6; \'sigmoid\')',
                         'change_activation_function_softmax_6': 'ACH (l6; \'softmax\')',
                         'change_activation_function_softplus_6': 'ACH (l6; \'softplus\')'}

    instance_names = ['TCL (84.38\%)', 'TRD (89.72\%)', 'TUD (90.62\%)', 'TAN (100\%)', 'TCO (96.88\%)',
                      'HLR (0.064)', 'HNE (1)', 'OCH (\'rmsprop\')', 'WCI (l0; \'ones\')',
                      'RAW (l0; \'l1\_l2\')', 'ARM (l5)', 'ACH (l6; \'sigmoid\')']

    for file in glob.glob(os.path.join(directory, '*')):
        output_file = os.path.join(file, 'leave_one_out.csv')
        data = pd.read_csv(output_file, nrows=10, names=["Killed", "Input_Num", "p_value", "effect_size"])
        counts = data["Killed"].value_counts()
        true_num = 0 if True not in counts.keys() else counts[True]
        input_mean = round(data["Input_Num"].mean())
        file_name = file.replace(directory, "")
        print(abbreviation_dict[file_name], '&', true_num, '&', input_mean, '\\\\')

