from os.path import exists
from properties import RESULTS_PATH, INTERPRETER, NUM_RUNS
import shutil
import time
from os import makedirs
import subprocess
import re

src = RESULTS_PATH

for i in range(NUM_RUNS):
    with open("properties.py", "r") as file_obj:
        #file_obj.write(pop_string)
        data = file_obj.read()

    with open("properties.py", "w") as file_obj:
        data = re.sub(r'DATASET = \"population_\d\"', 'DATASET = \"population_'+str(i)+'\"', data)
        file_obj.write(data)

    subprocess.call([INTERPRETER, "main.py"])

    #timestr = str(time.strftime("%Y%m%d-%H%M%S"))
    #dst = src+timestr
    dst = src + str(i)

    if not exists(dst):
        makedirs(dst)

    shutil.move(src, dst)
