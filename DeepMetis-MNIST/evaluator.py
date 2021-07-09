import numpy as np

from utils import get_distance
from properties import K


class Evaluator:
    cache = dict()

    # calculate the misclassification ff
    def evaluate_ff(self, confidence):
        if confidence < 0.0:
            confidence = -1.0
        return confidence

    def calculate_dist(self, ind, ind_pop):

        def memoized_dist(ind, ind_pop):
            index_str = tuple(sorted([ind.id, ind_pop.id]))
            if index_str in Evaluator.cache:
                return Evaluator.cache[index_str]
            d = get_distance(ind.member.purified, ind_pop.member.purified)
            Evaluator.cache.update({index_str: d})
            return d

        return memoized_dist(ind, ind_pop)

    def dist_from_nearest_archived(self, ind, population, k):
        neighbors = list()
        for ind_pop in population:
            if ind_pop.id != ind.id:
                d = self.calculate_dist(ind, ind_pop)
                if d > 0.0:
                    neighbors.append(d)

        if len(neighbors) == 0:
            assert (len(population) > 0)
            assert (population[0].id == ind.id)
            return -1.0

        neighbors.sort()
        nns = neighbors[:k]
        if k > 1:
            dist = np.mean(nns)
        elif k == 1:
            dist = nns[0]
        if dist == 0.0:
            print('bug')
        return dist


    def evaluate_sparseness(self, ind, individuals):
        N = (len(individuals))
        # Sparseness is evaluated only if the archive is not empty
        # Otherwise the sparseness is 1
        if (N == 0) or (N == 1 and individuals[0] == ind):
            sparseness = 1
        else:
            sparseness = self.dist_from_nearest_archived(ind, individuals, K)
        return sparseness
