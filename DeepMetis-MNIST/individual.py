import numpy as np
from tensorflow import keras

from evaluator import Evaluator
import predictor
import mutant_predictor
from properties import MODELS, MUT_MODELS
import glob


class Individual(object):
    # Global counter of all the individuals (it is increased each time an individual is created or mutated).
    COUNT = 0
    SEEDS = set()

    def __init__(self, member, seed):
        self.id = Individual.COUNT
        self.seed = seed
        self.sparseness = None
        self.ff = None
        self.member = member
        self.filterin = False
        self.filterout = False
        self.eva = Evaluator()


    def reset(self):
        self.id = Individual.COUNT
        self.sparseness = None
        self.ff = None
        self.filterin = False
        self.filterout = False

    def evaluate(self, archive):
        self.sparseness = None

        if self.ff is None:
            self.ff = 0
            for i in range(len(glob.glob(MUT_MODELS + '/*.h5'))):
                #predicted_label, P_class, P_notclass = \
                #    mutant_predictor.Predictor.predict(i, self.member.purified, self.member.expected_label)
                # Calculate fitness function
                ff = self.eva.evaluate_ff(self.member.confidence[i])
                if ff < 0.0 and self.filterin == False:
                    self.filterin = True
                self.ff += ff

            #if self.filterin == True:
            #    evaluation = self.eva.evaluate_ff(self.member.confidence_original)
            #    if evaluation < 0.0:
            #        self.filterin = False
            #        self.filterout = True

            # # solution 1
            if self.filterin == True:
                condition = True
                index = 0
                while(condition):
                    evaluation = self.eva.evaluate_ff(self.member.confidence_original[index])
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
            print(self.sparseness)
            print("BUG")

        return self.ff, self.sparseness
