import math
import copy
import numpy as np
from collections import defaultdict


class PopularityDst():
    def __init__(self, alpha):
        self.alpha = alpha        

    def assignPopularities(self, objects):
        self.pop_dst = []
        self.loc_frac = []
        for i in range(len(objects)):
            p = float(1)/math.pow(i + 1, self.alpha)
            self.pop_dst.append(p)

        size_pop = defaultdict(lambda : 0)
        for i in range(len(objects)):
            size_pop[objects[i]] += self.pop_dst[i]

        obj_sizes = list(size_pop.keys())
        obj_sizes.sort()

        pr_o = []
        for o in obj_sizes:
            pr_o.append(o*size_pop[o])
            #pr_o.append(o)
        self.obj_sizes = obj_sizes

        sum_frac = sum(pr_o)
        self.loc_frac = [float(x)/sum_frac for x in pr_o]
        self.loc_frac = np.cumsum(self.loc_frac)        

        sum_pop = sum(self.pop_dst)
        self.pop_dst = [float(x)/sum_pop for x in self.pop_dst]
        self.pop = copy.deepcopy(self.pop_dst)
        self.pop_dst = np.cumsum(self.pop_dst)


    def sample(self):
        z = np.random.random()

        obj = len(self.pop_dst) - 1
        pr = 0

        for i in range(len(self.pop_dst)):            
            if self.pop_dst[i] > z:
                obj = i
                break
        return obj


    def get_trace(self, objects, len):
        loc_frac = self.assignPopularities(objects)
        trace = []
        for i in range(len):
            req = self.sample()
            trace.append(req)
        return trace, self.loc_frac, self.obj_sizes
            

    def getDelta(self, objects,min_fd, max_fd):
        probabilities = []
        d_vals = []

        for d in range(min_fd, max_fd):
            prob = 0
            for i in range(len(objects)):
                sz = objects[i]
                p = self.pop[i]                
                if sz > abs(d):
                    prob += (p * sz) * (float(1)/(1 + sz)) * (1 - float(abs(d))/sz)
        
            probabilities.append(prob)
            d_vals.append(d)

        sum_p = sum(probabilities)
        print("sum _p ", sum_p)
        probabilities = [float(p)/sum_p for p in probabilities]
        probabilities_sum = np.cumsum(probabilities)

        return probabilities_sum, d_vals, probabilities
        
