import json
import sys
from os import makedirs
from os.path import exists


from utils import get_distance
import numpy as np

from properties import ARCHIVE_THRESHOLD, RESULTS_PATH, POPSIZE, NGEN, MUTLOWERBOUND, MUTUPPERBOUND, RESEEDUPPERBOUND, \
    MODELS, MAX_BUCKET_SIZE


class Archive:

    def __init__(self):
        self.archive = list()
        self.archived_seeds = set()
        self.tshd_members = dict()

    def get_archive(self):
        return self.archive

    def update_archive(self, ind):
        if ind not in self.archive:
            bucket = [arc_ind for arc_ind in self.archive if arc_ind.seed == ind.seed]
            if len(bucket) == 0:
                self.archive.append(ind)
                self.archived_seeds.add(ind.seed)
                self.tshd_members[ind.seed] = ind
            else:
                # Find the member of the archive that is closest to the candidate.
                d_min = np.inf
                i = 0
                while i < len(bucket):
                    distance_archived = get_distance(ind.member.purified, bucket[i].member.purified)
                    if distance_archived < d_min:
                        d_min = distance_archived
                    i += 1
                # Decide whether to add the candidate to the archive
                # Verify whether the candidate is close to the existing member of the archive
                # Note: 'close' is defined according to a user-defined threshold
                if d_min > 0.0:
                    if len(bucket) < MAX_BUCKET_SIZE:
                        #tshd = self.tshd_members[ind.seed]
                        #tshd = bucket[-1]
                        #if ind.ff > tshd.ff:
                        #    self.tshd_members[ind.seed] = ind
                        self.archive.append(ind)
                    elif len(bucket) == MAX_BUCKET_SIZE:
                        bucket.sort(key=lambda x: x.ff)
                        #print("MAX BUCKET SIZE")
                        #print("OLD TSHD: " + str(bucket[-1].id))
                        #tshd = self.tshd_members[ind.seed]
                        tshd = bucket[-1]
                        if ind.ff < tshd.ff:
                            self.tshd_members[ind.seed] = ind
                            self.archive.remove(tshd)
                            #print("REMOVE "+str(tshd.id))
                            self.archive.append(ind)
                            #print("ADD " + str(ind.id))
                            #print("NEW TSHD: " + str(self.tshd_members[ind.seed].id))
                    #sorted_bucket = [i.ff for i in bucket]
                    #print(sorted_bucket)
                    #print("NEW TSHD: "+str(self.tshd_members[ind.seed].id))

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

        config = {
            'popsize': str(POPSIZE),
            'generations': str(NGEN),
            #'label': str(EXPECTED_LABEL),
            'archive tshd': str(ARCHIVE_THRESHOLD),
            'mut low': str(MUTLOWERBOUND),
            'mut up': str(MUTUPPERBOUND),
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

