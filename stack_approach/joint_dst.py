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
        overall_sz_dst = defaultdict(int)
        
        for l in f:
            l = l.strip().split(" ")

            if len(l) == 1:
                key = int(l[0])
                sum_pop += key
                continue

            sz = int(l[0]) + 1
            objs = int(l[1])
            pop_sz[key][sz] += objs
            total_obj += objs

            overall_sz_dst[sz] += 1

        f.close()

        print("t objects : ", total_obj)

        self.pop_sz_vals = defaultdict(lambda : list)
        self.pop_sz_prs = defaultdict(lambda : list)

        sum_n_key = 0

        for key in pop_sz:
            sizes = list(pop_sz[key].keys())
            #sizes.sort()            
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
        self.sample_each_popularity()

        szs = list(overall_sz_dst.keys())
        szs.sort()
        counts = []
        for sz in szs:
            counts.append(overall_sz_dst[sz])
        sum_counts = sum(counts)
        counts = [float(x)/sum_counts for x in counts]
        counts = np.cumsum(counts)
        
        plt.plot(szs, counts)
        plt.grid()
        plt.savefig("overall_size_dst.png")
        plt.clf()

    def sample_each_popularity(self):
        self.samples = defaultdict(list)
        self.sampled_sizes = defaultdict(list)
        for k in self.pop_sz_prs:
            self.sampled_sizes[k] = np.random.choice(self.pop_sz_vals[k], 10000, p=self.pop_sz_prs[k])

        self.samples_index = defaultdict(int)
        self.popularities = list(self.pop_sz_prs.keys())
        self.popularities.sort()
        print(self.popularities[0], self.popularities[-1])

    def findnearest(self, k):
        ind = bisect.bisect_left(self.popularities, k)
        if ind >= len(self.popularities):
            ind = len(self.popularities) - 1
        return self.popularities[ind]

    def sample(self, k):
        k = self.findnearest(k)
        curr_index = self.samples_index[k]

        if curr_index >= len(self.sampled_sizes[k]):
            self.sampled_sizes[k] = np.random.choice(self.pop_sz_vals[k], 10000, p=self.pop_sz_prs[k])
            self.samples_index[k] = 0
            curr_index = 0

        self.samples_index[k] += 1        
        return int(self.sampled_sizes[k][curr_index])
        #return (int(self.sampled_sizes[k][curr_index%50000])/10) + 1
                    
    def sample_popularities(self, n):
        return np.random.choice(self.popularities, n, p=self.popularities)
           

class pop:
    def __init__(self, i_file):
        f = open(i_file, "r")
        self.popularities = defaultdict(int)

        l = f.readline()
        key = int(l.strip())
        sum_count = 0

        for l in f:
            l = l.strip().split(" ")
            if len(l) == 1:
                self.popularities[key] = sum_count
                sum_count = 0
                key = int(l[0])
            else:
                sum_count += int(l[1])
                
        p_keys = list(self.popularities.keys())
        vals = []
        for k in p_keys:
            vals.append(self.popularities[k])

        sum_vals = sum(vals)
        vals = [float(x)/sum_vals for x in vals]
        
        self.p_keys = p_keys
        self.pr = vals

                
    def sample_popularities(self, n):
        return np.random.choice(self.p_keys, n, p=self.pr)

            
            
            
            

        


            
        
