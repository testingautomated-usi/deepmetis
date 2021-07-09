import os
import random
import glob
import time
import csv

import h5py

import mutant_predictor, predictor
import vectorization_tools
from digit_input import Digit
from digit_mutator import DigitMutator
from utils import print_archive

import numpy as np
from deap import base, creator, tools
from deap.tools.emo import selNSGA2
from tensorflow import keras

import archive_manager
from individual import Individual
from properties import NGEN, IMG_SIZE, \
    POPSIZE, INITIALPOP, DATASET, RESEEDUPPERBOUND, MUT_MODELS, MODELS

hf = h5py.File(DATASET, 'r')
x_test = hf.get('xn')
x_test = np.array(x_test)
y_test = hf.get('yn')
y_test = np.array(y_test)

# Fetch the starting seeds from file
starting_seeds = [i for i in range(len(y_test))]
random.shuffle(starting_seeds)
starting_seeds = starting_seeds[:POPSIZE]
# assert(len(starting_seeds) == POPSIZE)

# DEAP framework setup.
toolbox = base.Toolbox()
# Define a bi-objective fitness function.
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
# Define the individual.
creator.create("Individual", Individual, fitness=creator.FitnessMulti)


def generate_digit(seed):
    seed_image = x_test[int(seed)]
    label = y_test[int(seed)]
    xml_desc = vectorization_tools.vectorize(seed_image)
    return Digit(xml_desc, label)


def generate_individual():
    Individual.COUNT += 1

    if INITIALPOP == 'random':
        # Choose randomly a file in the original dataset.
        seed = random.choice(starting_seeds)
        Individual.SEEDS.add(seed)
    elif INITIALPOP == 'seeded':
        # Choose sequentially the inputs from the seed list.
        # NOTE: number of seeds should be no less than the initial population
        assert (len(starting_seeds) == POPSIZE)
        seed = starting_seeds[Individual.COUNT - 1]
        Individual.SEEDS.add(seed)

    digit1 = generate_digit(seed)

    DigitMutator(digit1).mutate()

    individual = creator.Individual(digit1, seed)
    return individual


# TODO: reseeding
def reseed_individual(seeds):
    Individual.COUNT += 1
    # Chooses randomly the seed among the ones that are not covered by the archive
    # if len(starting_seeds) > len(seeds):
    #    chosen_seed = random.sample(set(starting_seeds) - seeds, 1)[0]
    # else:
    chosen_seed = random.choice(starting_seeds)

    digit = generate_digit(chosen_seed)

    DigitMutator(digit).mutate()

    individual = creator.Individual(digit, chosen_seed)
    return individual


# Evaluate an individual.
def evaluate_individual(individual, current_solution):
    individual.evaluate(current_solution)
    return individual.ff, individual.sparseness


def mutate_individual(individual):
    Individual.COUNT += 1
    DigitMutator(individual.member).mutate()
    individual.reset()


toolbox.register("individual", generate_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate_individual)
toolbox.register("select", selNSGA2)
toolbox.register("mutate", mutate_individual)


def pre_evaluate_batch(invalid_ind):
    batch_img = [i.member.purified for i in invalid_ind]
    batch_img = np.reshape(batch_img, (-1, 28, 28, 1))
    batch_label = np.array([i.member.expected_label for i in invalid_ind])

    for i in range(len(glob.glob(MUT_MODELS + '/*.h5'))):
        predictions, confidences = (mutant_predictor.Predictor.predict(i, batch_img,
                                                                       batch_label))

        for ind, confidence, prediction in zip(invalid_ind, confidences, predictions):
            ind.member.confidence.append(confidence)
            ind.member.predicted_label.append(prediction)

    for i in range(len(glob.glob(MODELS + '/*.h5'))):
        predictions, confidences = (predictor.Predictor.predict(i, batch_img,
                                                                batch_label))

        for ind, confidence, prediction in zip(invalid_ind, confidences, predictions):
            ind.member.confidence_original.append(confidence)
            ind.member.predicted_label_original.append(prediction)

    # predictions, confidences = (predictor.Predictor.predict(0, batch_img,
    #                                                         batch_label))
    #
    # for ind, confidence, prediction in zip(invalid_ind, confidences, predictions):
    #     ind.member.confidence_original = confidence
    #     ind.member.predicted_label_original = prediction


def main(rand_seed=None):
    random.seed(rand_seed)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "min", "max", "avg", "std"

    # Generate initial population.
    print("### Initializing population ....")
    population = toolbox.population(n=POPSIZE)

    # Evaluate the individuals with an invalid fitness.
    # Note: the fitnesses are all invalid before the first iteration since they have not been evaluated
    invalid_ind = [ind for ind in population]

    to_evaluate_ind = [ind for ind in population if ind.ff is None]
    pre_evaluate_batch(to_evaluate_ind)

    # fitnesses = toolbox.map(toolbox.evaluate, invalid_ind, itertools.repeat(population))
    # Note: the sparseness is calculated wrt the archive. It can be calculated wrt population+archive
    # Therefore, we pass to the evaluation method the current archive.
    fitnesses = [toolbox.evaluate(i, archive.get_archive()) for i in invalid_ind]
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # Update archive with the individuals on the decision boundary.
    for ind in population:
        if ind.filterin:
            # if ind.member.predicted_label == EXPECTED_LABEL and ind.member.mut_predicted_label != EXPECTED_LABEL:
            archive.update_archive(ind)

    print("### Number of Individuals generated in the initial population: " + str(Individual.COUNT))

    # This is just to assign the crowding distance to the individuals (no actual selection is done).
    population = toolbox.select(population, len(population))

    record = stats.compile(population)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    for gen in range(1, NGEN):
        # Vary the population.
        offspring = tools.selTournamentDCD(population, len(population))
        offspring = [toolbox.clone(ind) for ind in offspring]

        # Reseeding
        if len(archive.get_archive()) > 0:
            seed_range = random.randrange(1, RESEEDUPPERBOUND)
            candidate_seeds = archive.archived_seeds
            for i in range(seed_range):
                population[len(population) - i - 1] = reseed_individual(candidate_seeds)

            for i in range(len(population)):
                if population[i].filterout == True:
                    population[i] = reseed_individual(candidate_seeds)

        # Mutation.
        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        # Evaluate the individuals
        # NOTE: all individuals in both population and offspring are evaluated to assign crowding distance.
        invalid_ind = [ind for ind in population + offspring]
        pre_evaluate_batch(invalid_ind)

        fitnesses = [toolbox.evaluate(i, archive.get_archive()) for i in invalid_ind]
        # fitnesses = toolbox.map(toolbox.evaluate, invalid_ind, itertools.repeat(archive.get_archive()))

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        for ind in population + offspring:
            # if ind.fitness.values[0] < 0:
            if ind.filterin:
                # if ind.member.predicted_label == EXPECTED_LABEL and ind.member.mut_predicted_label != EXPECTED_LABEL:
                archive.update_archive(ind)

        # Select the next generation population
        population = toolbox.select(population + offspring, POPSIZE)

        if gen % 300 == 0:
            archive.create_report(gen)

        # print_generations(gen, population)

        # Update the statistics with the new population
        # record = stats.compile(pop) if stats is not None else {}
        if gen % 1 == 0:
            record = stats.compile(population)
            logbook.record(gen=gen, evals=len(invalid_ind), **record)
            print(logbook.stream)

    # print_generations('last', population)
    print(logbook.stream)

    return population


def get_elem(i):
    elem = (np.expand_dims(x_test[i], 0))
    if keras.backend.image_data_format() == 'channels_first':
        elem = elem.reshape(elem.shape[0], 1, IMG_SIZE, IMG_SIZE)
    else:
        elem = elem.reshape(elem.shape[0], IMG_SIZE, IMG_SIZE, 1)
    elem = elem.astype('float32')
    elem = elem / 255.0
    return elem


if __name__ == "__main__":
    time1 = time.time()
    archive = archive_manager.Archive()
    pop = main()

    print_archive(archive.get_archive())
    archive.create_report('final')
    time2 = time.time()
    elapsed_time = (time2 - time1)

    num_generated_inputs = len(glob.glob1('results/archive/', "*.npy"))

    info_file = 'info.csv'

    if os.path.exists(info_file):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not

    with open(info_file, append_write) as f1:
        writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
        writer.writerow([str(elapsed_time), str(num_generated_inputs)])
print("GAME OVER")
