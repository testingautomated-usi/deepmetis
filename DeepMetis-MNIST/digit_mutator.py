import random
import mutation_manager
import rasterization_tools
import vectorization_tools
from digit_input import Digit
from properties import MUTOPPROB
from utils import get_distance


class DigitMutator:

    def __init__(self, digit):
        self.digit = digit

    def mutate(self, reference=None):
        # Select mutation operator.
        rand_mutation_probability = random.uniform(0, 1)
        if rand_mutation_probability >= MUTOPPROB:
            mutation = 1
        else:
            mutation = 2

        condition = True
        counter_mutations = 0
        while condition:
            counter_mutations += 1
            mutant_vector = mutation_manager.mutate(self.digit.xml_desc, mutation, counter_mutations/20)
            mutant_xml_desc = vectorization_tools.create_svg_xml(mutant_vector)
            rasterized_digit = rasterization_tools.rasterize_in_memory(mutant_xml_desc)

            distance_inputs = get_distance(self.digit.purified, rasterized_digit)

            if distance_inputs != 0:
                if reference is not None:
                    distance_inputs = get_distance(reference.purified, rasterized_digit)
                    if distance_inputs != 0:
                        condition = False
                else:
                    condition = False

        self.digit.xml_desc = mutant_xml_desc
        self.digit.purified = rasterized_digit
        # TODO
        self.digit.confidence = list()
        self.digit.predicted_label = list()
        self.digit.confidence_original = list()
        self.digit.predicted_label_original = list()

        return distance_inputs


