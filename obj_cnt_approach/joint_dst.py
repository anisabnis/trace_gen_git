import numpy as np
import json
from collections import defaultdict
from util import *
import matplotlib.pyplot as plt
import bisect

class pop_sz_dst:
    def __init__(self, i_file):
        pop_sz = defaultdict(lambda : defaultdict(int))        

        f = open(i_file, "r") 
        key = "-"
        t_pop = 0
        sum_pop = 0
        total_obj = 0

        for l in f:
            l = l.strip().split(" ")

            if len(l) == 1:
                key = int(l[0])
                sum_pop += key
                continue

            sz = int(l[0])
            objs = int(l[1])
            pop_sz[key][sz] += objs
            total_obj += objs

        f.close()

        print("t objects : ", total_obj)

        self.pop_sz_vals = defaultdict(lambda : list)
        self.pop_sz_prs = defaultdict(lambda : list)

        sum_n_key = 0

        for key in pop_sz:
            sizes = list(pop_sz[key].keys())
            sizes.sort()
            n_key = float(key)/sum_pop

            self.pop_sz_vals[n_key] = sizes
            sum_n_key += n_key
            prs = []
            for s in sizes:
                prs.append(pop_sz[key][s])
            sum_prs = sum(prs)
            prs = [float(x)/sum_prs for x in prs]
            self.pop_sz_prs[n_key] = prs

        print("sum : ", sum_n_key)

    def sample_each_popularity(self):
        self.samples = defaultdict(list)
        for k in self.pop_sz_prs:
            self.sampled_sizes[k] = np.random.choice(self.pop_sz_vals[k], 50000, p=self.pop_sz_prs[k])

        self.samples_index = defaultdict(int)
        self.popularities = list(self.pop_sz_prs.keys())
        self.popularities.sort()

    def findnearest(self, k):
        ind = bisect.bisect_left(self.popularities, k)
        return self.popularities[ind]

    def sample(self, k):
        k = self.findnearest(k)
        curr_index = self.samples_index[k]
        self.samples_index[k] += 1        
        return self.sampled_sizes[k][curr_index]
        
            
           


            
            
            
            

        


            
        
