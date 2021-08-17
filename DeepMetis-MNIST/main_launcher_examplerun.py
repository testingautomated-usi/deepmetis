from os.path import exists
from properties import RESULTS_PATH, INTERPRETER
import shutil
import time
from os import makedirs, remove
import subprocess
import glob
import argparse
import os

src = RESULTS_PATH

index =  0
#for mutant in ('mnist_add_noise_mutated0_MP_100_', 'mnist_change_epochs_mutated0_MP_1_', 'mnist_change_learning_rate_mutated0_MP_False_0.064_', 'mnist_change_label_mutated0_MP_84.38_'):
#for mutant in ('mnist_delete_training_data_mutated0_MP_89.72_', 'mnist_unbalance_train_data_mutated0_MP_90.62_', 'mnist_make_output_classes_overlap_mutated0_MP_96.88_'): 
#'mnist_change_activation_function_mutated0_MP_sigmoid_6_', 'mnist_remove_activation_function_mutated0_MP_5_',
parser = argparse.ArgumentParser()
parser.add_argument("--run_type", "-run_type",
                        type=str, help="type of run")
parser.add_argument("--mutant_num", "-mutant_num", default=5, 
                        type=int, help="number of mutant instances")
parser.add_argument("--run_num", "-run_num", default=1,
                        type=int, help="number of runs")
args = parser.parse_args()

run_type = args.run_type
mutant_num = args.mutant_num
mutant_list = ('mnist_add_weights_regularisation_mutated0_MP_l1_l2_0_',)
run_num = args.run_num

if run_type == 'full':
   run_num = 10
   mutant_list = ('mnist_change_optimisation_function_mutated0_MP_rmsprop_', 'mnist_change_weights_initialisation_mutated0_MP_ones_0_', 'mnist_add_weights_regularisation_mutated0_MP_l1_l2_0_', 'mnist_add_noise_mutated0_MP_100_', 'mnist_change_epochs_mutated0_MP_1_', 'mnist_change_learning_rate_mutated0_MP_False_0.064_', 'mnist_change_label_mutated0_MP_84.38_', 'mnist_delete_training_data_mutated0_MP_89.72_', 'mnist_unbalance_train_data_mutated0_MP_90.62_', 'mnist_make_output_classes_overlap_mutated0_MP_96.88_', 'mnist_change_activation_function_mutated0_MP_sigmoid_6_', 'mnist_remove_activation_function_mutated0_MP_5_')

print(run_num, mutant_num, mutant_list)
for mutant in mutant_list:  
    files = glob.glob('mutant_model/*')
    for f in files:
        print("removing", f)
        remove(f)
    for j in range(0, mutant_num):
        shutil.copyfile('models/' + mutant + str(j) + '.h5', 'mutant_model/' + mutant + str(j) + '.h5')
    for i in range(0, run_num):
       #print(mutant, i, nums[index])
   #subprocess.call([INTERPRETER, "metis_pop_generator3.py"])
       shutil.copyfile('populations/metis_dataset' + str(i) + '.h5', 'original_dataset/metis_dataset.h5')
       subprocess.call([INTERPRETER, "main.py"])

       dst = src+'_'+mutant+str(run_num)
       #timestr = str(time.strftime("%Y%m%d-%H%M%S"))
       #dst = src+timestr
       if os.path.exists(dst):
           shutil.rmtree(dst)

       if not exists(dst):
           makedirs(dst)

       shutil.move(src, dst)
    index = index + 1
