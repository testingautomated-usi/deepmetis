from properties import MODELS, MUT_MODELS
import glob
from evaluator import Evaluator


class Individual(object):
    # Global counter of all the individuals (it is increased each time an individual is created or mutated).
    COUNT = 0
    SEEDS = set()

    def __init__(self, member, seed):
        self.id = Individual.COUNT
        self.seed = seed
        self.sparseness = None
        self.ff = None
        self.ff_boundless = None
        self.member = member
        self.filterin = False
        self.filterout = False
        self.eva = Evaluator()


    def reset(self):
        self.id = Individual.COUNT
        self.sparseness = None
        self.ff_boundless = None
        self.ff = None
        self.filterin = False
        self.filterout = False

    def evaluate(self, archive):
        self.sparseness = None

        if self.ff is None:
            self.ff = 0
            # TODO
            self.ff_boundless = 0
            for i in range(len(glob.glob(MUT_MODELS + '/*.h5'))):
                ff = self.eva.evaluate_ff(self.member.diff[i])
                # TODO
                ff_boundless = self.member.diff[i]
                if ff < 0.0 and self.filterin == False:
                    self.filterin = True
                self.ff += ff
                # TODO
                self.ff_boundless += ff_boundless


            if self.filterin == True:
                condition = True
                index = 0
                while(condition):

                    evaluation = self.eva.evaluate_ff(self.member.diff_original[index])

                    index += 1
                    if evaluation < 0.0:
                        condition = False
                        self.filterin = False
                        self.filterout = True
                    elif index == len(glob.glob(MODELS + '/*.h5')):
                        condition = False

        # Recalculate sparseness at each iteration
        self.sparseness = self.eva.evaluate_sparseness(self, archive)
        if self.sparseness == 0.0:
            print("BUG")

        return self.ff, self.sparseness
