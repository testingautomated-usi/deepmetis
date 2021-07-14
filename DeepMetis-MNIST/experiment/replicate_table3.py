import os
import csv
import pandas as pd
import numpy as np


def get_operator_type(operator):
    if operator in ('add_noise', 'change_epochs', 'change_label', 'change_learning_rate',
                    'delete_training_data', 'make_output_classes_overlap', 'unbalance_train_data'):
        return 'C'
    else:
        return 'NC'


def get_upper_bound(operator):
    if operator in ('add_noise', 'change_label', 'make_output_classes_overlap', 'unbalance_train_data'):
        return 100
    elif operator == 'delete_training_data':
        return 99
    elif operator == 'change_epochs':
        return 1
    elif operator == 'change_learning_rate':
        return 0.001


def get_train_killed(operator):
    kill_conf_dict = {'add_noise': 43.75, 'change_label': 3.12, 'make_output_classes_overlap': 25.00,
                      'unbalance_train_data': 9.38, 'delete_training_data': 3.1, 'change_epochs': 10,
                      'change_learning_rate': 0.812}

    return kill_conf_dict[operator]


def get_abbreviation(full_name):
    abbreviation_dict = {'add_noise': 'TAN', 'change_label': 'TCL', 'make_output_classes_overlap': 'TCO',
                         'unbalance_train_data': 'TUD', 'delete_training_data': 'TRD', 'change_epochs': 'HNE',
                         'change_learning_rate': 'HLR', 'change_optimisation_function': 'OCH',
                         'remove_activation_function': 'ARM',  'change_weights_initialisation': 'WCI',
                         'add_weights_regularisation': 'RAW', 'change_activation_function': 'ACH',
                         'deepmetis/deepmetis_1vs1/': 'DM1vs1',
                         'deepmetis/deepmetis_1vs5/': 'DM1vs5', 'deepmetis/deepmetis_1vs10/': 'DM1vs10',
                         'deepmetis/deepmetis_1vs20/': 'DM1vs20', 'deepjanus/': 'DJ', 'dlfuzz/only_valid_inputs/': 'DF'}

    return abbreviation_dict[full_name]


def get_overall_results_file(operator, file_dir):
    output_file = os.path.join(file_dir, 'output.csv')
    operator_type = get_operator_type(operator)

    if not os.path.exists(output_file):
        print(output_file, "does not exist")
        return

    data = pd.read_csv(output_file)
    #print(output_file, data['Input Num'])

    if data.shape[0] != 10 or (data.shape[1] not in (3, 5)):
        print("wrong shape for file", output_file, data.shape)
        return

    index_row = 'Run Num' if operator_type == 'NC' else 'Population'
    killing_row = 'WLX Killed' if operator_type == 'NC' else 'Killed Conf'

    data.set_index(index_row)
    data.sort_index()

    assert (len(data[killing_row]) == 10)
    input_mean = data['Input Num'].mean()

    if operator_type == 'NC':
        counts = data[killing_row].value_counts()
        true_num = 0 if True not in counts.keys() else counts[True]
        return data['Input Num'], data[killing_row], true_num / 10
    else:
        upper_bound = get_upper_bound(operator)
        train_killed_conf = get_train_killed(operator)
        mut_score = round((upper_bound - data[killing_row]) / (upper_bound - train_killed_conf), 2)
        mut_score[mut_score > 1.0] = 1.0
        #return np.mean(mut_score), input_mean, data['Input Num'], mut_score
        return data['Input Num'], mut_score, np.mean(mut_score)


def get_summary_file():
    csv_file = os.path.join(directory, "summary.csv")

    if os.path.exists(csv_file):
        os.remove(csv_file)

    ind = 0
    for operator in operators:
        csv_row = []
        table_row = instance_names[ind] + " & " + initial_mutation_score[ind]
        csv_row.append(instance_names[ind])
        csv_row.append(initial_mutation_score[ind])
        for subdir in sub_dirs:
            file_dir = os.path.join(directory, subdir, operator)
            input_num, mut_score, input_mean = get_overall_results_file(operator, file_dir)
            mut_score_mean = np.mean(mut_score)
            input_num_mean = np.mean(input_num)
            table_row = table_row + " & " + str(round(input_num_mean)) + " & " + str(round(mut_score_mean * 100)) + "\%"
            csv_row.append(round(input_mean))
            csv_row.append(mut_score_mean)
        print(table_row + "\\\\")
        ind = ind + 1

        with open(csv_file, 'a') as f1:
            writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
            writer.writerow(csv_row)


def get_raw_data():
    raw_data_csv = os.path.join(directory, "raw_data.csv")

    if os.path.exists(raw_data_csv):
        os.remove(raw_data_csv)

    data = None

    for operator in operators:
        operator_type = get_operator_type(operator)

        if operator_type == 'C' or operator_type == 'NC':
            operator_short_name = get_abbreviation(operator)
            for subdir in sub_dirs:
                dir_short_name = get_abbreviation(subdir)
                file_dir = os.path.join(directory, subdir, operator)
                input_num, mut_score, average = get_overall_results_file(operator, file_dir)
                suffix = operator_short_name + "_" + dir_short_name

                if data is None:
                    data = pd.DataFrame({suffix + "_I": input_num})
                else:
                    input_column = pd.DataFrame({suffix + "_I": input_num})
                    data = data.join(input_column)

                mut_column = pd.DataFrame({suffix + "_MS": mut_score})
                data = data.join(mut_column)

    data.to_csv(raw_data_csv)


if __name__ == '__main__':
    directory = ""
    sub_dirs = ["deepmetis/deepmetis_1vs1/", "deepmetis/deepmetis_1vs5/",
                "deepmetis/deepmetis_1vs10/", "deepmetis/deepmetis_1vs20/",
                "deepjanus/", "dlfuzz/only_valid_inputs/"]
    operators = ['change_label', 'delete_training_data', 'unbalance_train_data',
                 'add_noise', 'make_output_classes_overlap', 'change_learning_rate',
                 'change_epochs', 'change_optimisation_function', 'change_weights_initialisation',
                 'add_weights_regularisation', 'remove_activation_function', 'change_activation_function']

    instance_names = ['TCL (84.38\%)', 'TRD (89.72\%)', 'TUD (90.62\%)', 'TAN (100\%)', 'TCO (96.88\%)',
                      'HLR (0.064)', 'HNE (1)', 'OCH (\'rmsprop\')', 'WCI (l0; \'ones\')',
                      'RAW (l0; \'l1\_l2\')', 'ARM (l5)', 'ACH (l6; \'sigmoid\')']

    initial_mutation_score = ['13\%', '6\%', '6\%', '0\%', '0\%', '0\%', '0\%', '0\%', '0\%', '0\%', '0\%', '0\%',
                              '0\%']

    get_raw_data()
    get_summary_file()
