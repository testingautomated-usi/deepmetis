import glob
import os
import csv
import pandas as pd


if __name__ == '__main__':
    directory = "leave_one_out_RQ4"
    abbreviation_dict = {'TCL': 'TCL (21.88\%)', 'TRD': 'TRD (41.66\%)', 'TUD': 'TUD (100\%)',
                      'TAN': 'TAN (84.38\%)',
                      'HLR': 'HLR (0.0037)', 'HNE': 'HNE (32)', 'AAL': 'AAL (l9; \'signsoft\')',
                      'RAW_L1': 'RAW (l1; \'l1\_l2\')', 'RAW_L3': 'RAW (l3; \'l1\_l2\')', 'WCI': 'WCI (l1; \'ones\')'}

    output_file = 'leave_one_out.csv'
    output = []

    for mo, mo_data in abbreviation_dict.items():
        data = pd.read_csv(os.path.join(directory, mo + ".csv"), nrows=10, names=["idx", "Input_Num", "Killed", "p_value", "effect_size"])
        counts = data["Killed"].value_counts()
        true_num = 0 if True not in counts.keys() else counts[True]
        input_mean = round(data["Input_Num"].mean())
        # row = [mo_data, '&', true_num, '&', input_mean, '\\\\']
        # print(mo_data, '&', true_num, '&', input_mean, '\\\\')
        row = [mo_data, input_mean, true_num]
        print(row)
        output.append(row)

    with open(output_file, 'a') as f1:
        writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
        writer.writerows(output)

