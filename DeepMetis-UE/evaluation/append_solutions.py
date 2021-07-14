import re
import numpy as np
import os
from glob import glob




def append_solutions(search_folder_name, solution_num):

    dataset_x_img = []
    dataset_x_head_angles = []
    dataset_y_gaze_angles = []

    files = glob(os.path.join(search_folder_name, search_params), recursive=True)

    # print("Current Solution "+str(solution_num))
    for file in files:
        file_name = file

        # parse file name
        file_name = file_name.replace(search_folder_name, "")

        fn = file_name.replace(".npy", "")
        # fn = fn.split("seed_1_")
        fn = fn.split("label")
        fn = fn[1].split("camera")
        lbl = fn[0].split("_")
        fn = re.split("seed_._", fn[1])
        cam = fn[0].split("_")

        x_img = np.load(file)
        x_img = np.squeeze(x_img, axis=0)
    #
        # append to dataset
        dataset_x_img.append(x_img)
    #
        h_a_1 = np.radians(int(cam[1]))
        h_a_2 = np.radians(int(cam[2]))
        g_a_1 = np.radians(int(lbl[1]))
        g_a_2 = np.radians(int(lbl[2]))

        dataset_x_head_angles.append([h_a_1, h_a_2])
        dataset_y_gaze_angles.append([g_a_1, g_a_2])



    # # convert to numpy array
    dataset_x_img_np = np.stack(dataset_x_img)
    dataset_x_head_angles_np = np.stack(dataset_x_head_angles)
    dataset_y_gaze_angles_np = np.stack(dataset_y_gaze_angles)

    # covert to float
    # dataset_x_img_np = dataset_x_img_np.astype('float32')
    dataset_x_head_angles_np = dataset_x_head_angles_np.astype('float32')
    dataset_y_gaze_angles_np = dataset_y_gaze_angles_np.astype('float32')

    global x_img_test, x_ha_test, y_gaze_test

    x_img_test_ext = np.concatenate((x_img_test, dataset_x_img_np), axis=0)
    x_ha_test_ext = np.concatenate((x_ha_test, dataset_x_head_angles_np), axis=0)
    y_gaze_test_ext = np.concatenate((y_gaze_test, dataset_y_gaze_angles_np), axis=0)

    x_img_name = os.path.join(output_folder, 'x_img_wts_' + operator + "_" + solution_num + '.npy')
    x_ha_name = os.path.join(output_folder, 'x_ha_wts_' + operator + "_" + solution_num + '.npy')
    y_gaze_name = os.path.join(output_folder, 'y_gaze_wts_' + operator + "_" + solution_num + '.npy')

    np.save(x_img_name, x_img_test_ext)
    np.save(x_ha_name, x_ha_test_ext)
    np.save(y_gaze_name, y_gaze_test_ext)


search_params = "*.npy"

dataset_folder = "datasets"

output_folder = "datasets"

x_img_test = np.load(os.path.join(dataset_folder, 'srch_img_10.npy'))
x_ha_test = np.load(os.path.join(dataset_folder, 'srch_ha_10.npy'))
y_gaze_test = np.load(os.path.join(dataset_folder, 'srch_gaze_10.npy'))

global operator, batch_num
operator = "AAL"
num_results = 1

results_folder = os.path.join("..", "results")

for i in range(num_results):
    search_folder_name = os.path.join(results_folder, "archive")
    try:
        append_solutions(search_folder_name, str(i))
    except ValueError as ve:
        if str(ve) == 'need at least one array to stack':
            print("Solution " + str(i) + " is empty!")
