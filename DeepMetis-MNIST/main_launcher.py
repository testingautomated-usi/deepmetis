from os.path import exists
from properties import RESULTS_PATH, INTERPRETER
import shutil
import time
from os import makedirs
import subprocess

src = RESULTS_PATH

for i in range(10):

   subprocess.call([INTERPRETER, "metis_pop_generator.py"])
   subprocess.call([INTERPRETER, "main.py"])

   dst = src+str()
   timestr = str(time.strftime("%Y%m%d-%H%M%S"))
   dst = src+timestr

   if not exists(dst):
       makedirs(dst)

   shutil.move(src, dst)
