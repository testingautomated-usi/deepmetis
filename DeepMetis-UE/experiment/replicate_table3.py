import os
import csv
import pandas as pd
import numpy as np


def get_operator_type(operator):
    if operator in ('add_noise', 'change_epochs', 'change_label', 'change_learning_rate',
                    'delete_training_data', 'unbalance_train_data'):
        return 'C'
    else:
        return 'NC'


def get_upper_bound(operator):
    if operator in ('add_noise', 'change_label', 'unbalance_train_data'):
        return 100
    elif operator == 'delete_training_data':
        return 99
    elif operator == 'change_epochs':
        return 1
    elif operator == 'change_learning_rate':
        return 0.001


def get_train_killed(operator):
    kill_conf_dict = {'add_noise': 50, 'change_label': 12.5,
                      'unbalance_train_data': 100, 'delete_training_data': 24.75, 'change_epochs': 41,
                      'change_learning_rate': 0.0066}

    return kill_conf_dict[operator]


def get_abbreviation(full_name):
    abbreviation_dict = {'add_noise': 'TAN', 'change_label': 'TCL',
                         'unbalance_train_data': 'TUD', 'delete_training_data': 'TRD', 'change_epochs': 'HNE',
                         'change_learning_rate': 'HLR',
                         'change_weights_initialisation': 'WCI',
                         'add_weights_regularisation_l3': 'RAW_L3', 'add_weights_regularisation_l1': 'RAW_L1',
                         'add_activation_function': 'AAL',
                         'deepmetis/deepmetis_1vs1/': 'DM1vs1',
                         'deepmetis/deepmetis_1vs5/': 'DM1vs5', 'deepmetis/deepmetis_1vs10/': 'DM1vs10',
                         'deepmetis/deepmetis_1vs20/': 'DM1vs20', 'deepjanus/': 'DJ',}

    return abbreviation_dict[full_name]


def get_overall_results_file(operator, file_dir):
    output_file = file_dir + 'output.csv'
    operator_type = get_operator_type(operator)

    if not os.path.exists(output_file):
        print(output_file, "does not exist")
        return

    data = pd.read_csv(output_file)

    if data.shape[0] != 10 or (data.shape[1] not in (3, 5)):
        print("wrong shape for file", output_file, data.shape)
        return

    index_row = 'Population'#'Run Num' if operator_type == 'NC' else 'Population'
    killing_row = 'Killed Conf'#'WLX Killed' if operator_type == 'NC' else 'Killed Conf'

    data.set_index(index_row)
    data.sort_index()

    assert (len(data[killing_row]) == 10)
    input_mean = data['Input Num'].mean()

    if operator_type == 'NC':
        counts = data[killing_row].value_counts()
        true_num = 0 if True not in counts.keys() else counts[True]
        return data['Input Num'], data[killing_row], true_num / 10, input_mean
    else:
        upper_bound = get_upper_bound(operator)
        train_killed_conf = get_train_killed(operator)

        killing = data[killing_row]
        denom = upper_bound - train_killed_conf
        if operator == "unbalance_train_data" and upper_bound == train_killed_conf:
            denom = upper_bound - train_killed_conf + 1
            killing = killing.replace("-", upper_bound * 2)
            killing = killing.replace("100", 100)
            upper_bound = upper_bound * 2

        mut_score = round((upper_bound - killing) / (denom), 2)
        print("MS", mut_score)
        mut_score[mut_score > 1.0] = 1.0
        # return np.mean(mut_score), input_mean, data['Input Num'], mut_score
        return data['Input Num'], mut_score, np.mean(mut_score), input_mean


def get_summary_file():
    csv_file = "summary.csv"

    ind = 0
    for operator in operators:
        csv_row = []
        table_row = instance_names[ind] + " & " + initial_mutation_score[ind]
        csv_row.append(instance_names[ind])
        csv_row.append(initial_mutation_score[ind])
        for subdir in sub_dirs:
            file_dir = subdir + operator + "/"
            input_num, mut_score, input_mean, inp_mean_true = get_overall_results_file(operator, file_dir)
            mut_score_mean = np.mean(mut_score)
            try:
                table_row = table_row + " & " + str(round(inp_mean_true)) + " & " + str(round(mut_score_mean * 100)) + "\%"
            except Exception as e:
                raise(e)
            csv_row.append(round(inp_mean_true))
            csv_row.append(mut_score_mean * 100)
        ind = ind + 1

        with open(csv_file, 'a') as f1:
            writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
            writer.writerow(csv_row)


def get_raw_data():
    raw_data_csv = "raw_data.csv"
    data = None

    for operator in operators:
        operator_type = get_operator_type(operator)

        if operator_type == 'C' or operator_type == 'NC':
            operator_short_name = get_abbreviation(operator)
            for subdir in sub_dirs:
                dir_short_name = get_abbreviation(subdir)
                file_dir = subdir + operator + "/"
                input_num, mut_score, ms_average, input_avg = get_overall_results_file(operator, file_dir)
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

    sub_dirs = ["deepmetis/deepmetis_1vs1/", "deepmetis/deepmetis_1vs5/",
                "deepmetis/deepmetis_1vs10/", "deepmetis/deepmetis_1vs20/",
                "deepjanus/"]

    operators = ['change_label', 'delete_training_data', 'unbalance_train_data',
                 'add_noise', 'change_learning_rate',
                 'change_epochs', 'add_activation_function',
                 'add_weights_regularisation_l1', 'add_weights_regularisation_l3', 'change_weights_initialisation']

    instance_names = ['TCL (21.88\%)', 'TRD (41.66\%)', 'TUD (100\%)',
                      'TAN (84.38\%)',
                      'HLR (0.0037)', 'HNE (32)', 'AAL (l9; \'signsoft\')',
                      'RAW (l1; \'l1\_l2\')', 'RAW (l3; \'l1\_l2\')', 'WCI (l1; \'ones\')']

    initial_mutation_score = ['86\%', '67\%', '0\%',
                              '25\%', '39\%', '70\%', '0\%', '0\%', '0\%', '0\%']

    get_raw_data()
    get_summary_file()
