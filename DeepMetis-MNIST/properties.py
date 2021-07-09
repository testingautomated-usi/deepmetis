# GA Setup
POPSIZE = 100
NGEN = 1000

# Mutation Hyperparameters
# range of the mutation
MUTLOWERBOUND = 0.1
MUTUPPERBOUND = 0.6

# Reseeding Hyperparameters
# extent of the reseeding operator
RESEEDUPPERBOUND = 10

# K-nearest
K = 1

# Archive configuration
ARCHIVE_THRESHOLD = 4.0
MAX_BUCKET_SIZE = 30

#------- NOT TUNING ----------

# mutation operator probability
MUTOPPROB = 0.5
MUTOFPROB = 0.5

IMG_SIZE = 28
num_classes = 10


INITIALPOP = 'seeded'

RESEED_STRATEGY = 'random'

GENERATE_ONE_ONLY = False

MODELS='original_models'
MUT_MODELS='mutant_models'

RESULTS_PATH = 'results'
DATASET = 'original_dataset/metis_dataset.h5'
INTERPRETER = 'python'