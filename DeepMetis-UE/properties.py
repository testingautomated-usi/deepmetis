import os

# GA Setup
POPSIZE = 12
NGEN = 100

MISB_TSHD = 5.0

# Reseeding Hyperparameters
# extent of the reseeding operator
RESEEDUPPERBOUND = 2

# K-nearest
K = 1

# Archive configuration
ARCHIVE_THRESHOLD = 0.7
#ARC_TYPE = "bound"
ARC_TYPE = "unbound"

#------- NOT TUNING ----------

# mutation operator probability
MUTOPPROB = 0.5
MUTOFPROB = 0.5

IMG_SIZE = 28
num_classes = 10


INITIALPOP = 'seeded'

RESEED_STRATEGY = 'random'

MODELS='original_models'
MUT_MODELS='mutant_models'

RESULTS_PATH = 'results'

DATASET = 'population_9'


SIKULIX_API_PATH = "Sikuli-jars//sikulixapi-2.0.4.jar"

SIKULIX_REST = "http://localhost:50001/"


SIKULIX_SCRIPT_FOLDER = os.path.join("C://","sikulix_scripts")

# BASEPATH = os.getcwd().replace("\\", "//")

#SIKULIX_SCRIPTS_HOME = BASEPATH + "//sikulix_scripts"
SIKULIX_SCRIPTS_HOME = "sikulix_scripts"

SIKULIX_SCRIPT_NAME = "unityeyes"

SIKULIX_SCRIPT_NAME_W_FMT = "unityeyes.sikuli"

SIKULIX_ANGLES_FILE_NAME = "angles.txt"

# TODO: modify unityeyes paths and interpreter
UNITYEYES_PATH = "C://Users//vinni//Desktop//UnityEyes//UnityEyes_Windows"
INTERPRETER = r'C:\Users\vinni\PycharmProjects\venvs\DeepMetis-UnityEyes\Scripts\python'

UNITY_GENERATED_IMGS_PATH = UNITYEYES_PATH + "//imgs_"
UNITY_STANDARD_IMGS_PATH = UNITYEYES_PATH + "//imgs//"

