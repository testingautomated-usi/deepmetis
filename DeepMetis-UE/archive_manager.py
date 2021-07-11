import json
from os import makedirs
from os.path import exists


import numpy as np

from distance_calculator import calc_distance_total
from properties import ARCHIVE_THRESHOLD, RESULTS_PATH, POPSIZE, NGEN, RESEEDUPPERBOUND, MISB_TSHD, ARC_TYPE


class Archive:

    def __init__(self):
        self.archive = list()
        self.archived_seeds = set()

    def get_archive(self):
        return self.archive

    def update_archive(self, ind):
        if ind not in self.archive:
            if len(self.archive) == 0:
                self.archive.append(ind)
                self.archived_seeds.add(ind.seed)
            else:
                # Find the member of the archive that is closest to the candidate.
                closest_archived = None
                d_min = np.inf
                i = 0
                while i < len(self.archive):
                    distance_archived = calc_distance_total(
                        ind.member.model_params,
                        self.archive[i].member.model_params)
                    if distance_archived < d_min:
                        closest_archived = self.archive[i]
                        d_min = distance_archived
                    i += 1
                # Decide whether to add the candidate to the archive
                # Verify whether the candidate is close to the existing member of the archive
                # Note: 'close' is defined according to a user-defined threshold
                if d_min <= ARCHIVE_THRESHOLD:
                    #assert(ind.seed == closest_archived.seed)
                    # The candidate replaces the closest archive member if its members' distance is better
                    if ARC_TYPE=="bound":
                        fitness_ind = ind.ff
                        fitness_archived_ind = closest_archived.ff
                    elif ARC_TYPE=="unbound":
                        fitness_ind = ind.ff_boundless
                        fitness_archived_ind = closest_archived.ff_boundless
                    if fitness_ind <= fitness_archived_ind:
                        self.archive.remove(closest_archived)
                        self.archive.append(ind)
                        self.archived_seeds.add(ind.seed)
                else:
                    # Add the candidate to the archive if it is distant from all the other archive members
                    self.archive.append(ind)
                    self.archived_seeds.add(ind.seed)



    def create_report(self, generation):
        # Retrieve the solutions belonging to the archive.
        solution = [ind for ind in self.archive]
        N = (len(solution))

        print("Final solution N is: " + str(N))

        final_seeds = self.get_seeds()
        stats = self.get_fitnesses()

        report = {
            'archive_len': str(N),
            'covered_seeds': len(self.archived_seeds),
            'final_seeds': len(final_seeds),
            'min_fitness':str(stats[0]),
            'max_fitness': str(stats[1]),
            'avg_fitness': str(stats[2]),
            'std_fitness': str(stats[3]),
        }

        if not exists(RESULTS_PATH):
            makedirs(RESULTS_PATH)
        #import time
        # timestr = time.strftime("%Y%m%d-%H%M%S")
        # dst = RESULTS_PATH+f'/report-{timestr}.json'
        dst = RESULTS_PATH + '/report_'+str(generation)+'.json'
        report_string = json.dumps(report)

        file = open(dst, 'w')
        file.write(report_string)
        file.close()

        #TODO: Change the bounds?
        config = {
            'popsize': str(POPSIZE),
            'generations': str(NGEN),
            'archive tshd': str(ARCHIVE_THRESHOLD),
            'misb_tshd': str(MISB_TSHD),
            'reseed': str(RESEEDUPPERBOUND),
            #'model': str(MODEL)
        }
        dst = RESULTS_PATH + '/config.json'
        config_string = json.dumps(config)

        file = open(dst, 'w')
        file.write(config_string)
        file.close()

    def get_seeds(self):
        seeds = set()
        for ind in self.get_archive():
            seeds.add(ind.seed)
        return seeds

    def get_fitnesses(self):
        fitnesses = list()
        stats = [None]*4

        for ind in self.get_archive():
            fitnesses.append(ind.ff)

        if len(fitnesses) > 0:
            stats[0] = np.min(fitnesses)
            stats[1] = np.max(fitnesses)
            stats[2] = np.mean(fitnesses)
            stats[3] = np.std(fitnesses)

        return stats

