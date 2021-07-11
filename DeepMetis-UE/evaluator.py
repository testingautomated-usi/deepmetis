import numpy as np

from distance_calculator import calc_distance_total, calc_angle_distance
from properties import K, MISB_TSHD


class Evaluator:
    cache = dict()

    def calculate_dist(self, ind, ind_pop):

        def memoized_dist(ind, ind_pop):
            index_str = tuple(sorted([ind.id, ind_pop.id]))
            if index_str in Evaluator.cache:
                return Evaluator.cache[index_str]
            result = calc_distance_total(ind.member.model_params, ind_pop.member.model_params)
            Evaluator.cache.update({index_str: result})
            return result
        return memoized_dist(ind, ind_pop)

    def evaluate_ff(self, ff):
        #diff = calc_angle_distance(pred, true)
        #diff = np.abs(np.degrees(diff))
        #ff = MISB_TSHD - diff
        if ff < 0.0:
            ff = -1.0
        return ff


    def dist_from_nearest_archived(self, ind, population, k):
        neighbors = list()
        for ind_pop in population:
            if ind_pop.id != ind.id:
                d = self.calculate_dist(ind, ind_pop)
                #d = calc_distance_total(ind.member.model_params, ind_pop.member.model_params)
                if d > 0.0:
                    neighbors.append(d)

        if len(neighbors) == 0:
            return -1.0

        neighbors.sort()
        assert(len(neighbors) > 0)
        nns = neighbors[:k]
        if k == 1:
            dist = nns[0]
        elif k > 1:
            dist = np.mean(nns)
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

if __name__ == "__main__":
    import glob
    DATA = 'eye_dataset/'
    from eye_input import Eye
    from os.path import splitext

    sample_list = glob.glob(DATA + '/*.jpg')

    pop = []
    for image_path in sample_list:
        path = splitext(image_path)
        json_path = path[0] + ".json"

        sample: Eye = Eye(json_path, image_path)
        pop.append(sample)

    ind = pop[0]
    archive = pop
    k = 1

    neighbors = list()
    for ind_pop in pop:
        if ind_pop != ind:
            d = calc_distance_total(ind.model_params, ind_pop.model_params)
            if d > 0.0:
                neighbors.append(d)
        else:
            print("skip duplicated")
    neighbors.sort()
    assert(len(neighbors) > 0)
    nns = neighbors[:k]
    if k > 1:
        dist = np.mean(nns)
    elif k == 1:
        dist = nns[0]
    if dist == 0.0:
        print('bug')

    print(dist)
