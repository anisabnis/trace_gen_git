from collections import defaultdict
#import matplotlib.pyplot as plt
from random import choices
from util import *
import numpy as np
import json
import bisect
import copy

class pop_sz_dst:

    def __init__(self, i_file, opp=False, upperlimit= -1, lowerlimit = -1):
        upperlimit = -1

        pop_sz = defaultdict(lambda : defaultdict(int))        

        f = open(i_file, "r")

        tmp_file = i_file.split("/")[-1]
        
        if tmp_file == "fd_final.txt" or tmp_file == "popularity_sd_pop.txt":
            l = f.readline()
            l = l.strip().split(" ")
            st = int(l[2])
            end = int(l[3])
            self.ttm = end - st
        else:
            self.ttm = 0
        
        key = "-"
        t_pop = 0
        sum_pop = 0
        total_obj = 0
        overall_sz_dst = defaultdict(int)

        keys_cnt = 0

        for l in f:

            l = l.strip().split(" ")

            if tmp_file != "fd_final.txt" and tmp_file != "popularity_sd_pop.txt":
                if len(l) == 1:
                    key = int(l[0])
                    sum_pop += key
                    keys_cnt += 1
                    continue
            else:
                if int(float(l[0])) != key:
                    key = int(float(l[0]))
                    sum_pop += key
                    keys_cnt += 1
                    continue
                    
            
            if upperlimit != -1 and sz > upperlimit:
                continue

            if tmp_file == "fd_final.txt" or tmp_file == "popularity_sd_pop.txt":
                objs = float(l[2])
                sz   = int(float(l[1]))
            else:
                objs = float(l[1])
                sz   = int(float(l[0])) + 1
                
            if opp == False:
                if key >= lowerlimit:
                    pop_sz[key][sz] += objs
            else:
                pop_sz[sz][key] += objs
                
            total_obj += objs                
            overall_sz_dst[sz] += 1

        f.close()
        
        print("t objects : ", total_obj, keys_cnt, sum_pop)
        
        self.pop_sz_vals = defaultdict(lambda : list)
        self.pop_sz_prs = defaultdict(lambda : list)

        sum_n_key = 0

        for key in pop_sz:
            sizes = list(pop_sz[key].keys())
            n_key = key

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
        
        #plt.plot(szs, counts)
        #plt.grid()
        #plt.savefig("overall_" + arg + "_dst.png")
        #plt.clf()

    def sample_each_popularity(self):
        self.samples = defaultdict(list)
        self.sampled_sizes = defaultdict(list)

        for k in self.pop_sz_prs:
            self.sampled_sizes[k] = choices(self.pop_sz_vals[k], weights=self.pop_sz_prs[k], k=10000)

        self.samples_index = defaultdict(int)
        self.popularities = list(self.pop_sz_prs.keys())
        self.popularities.sort()
        print(self.popularities[0], self.popularities[-1])

        to_plot = np.cumsum(self.popularities)
        #plt.clf()
        #plt.plot(to_plot)
        #plt.grid()
        #plt.savefig("pop_dst.png")
        #plt.clf()

    def findnearest(self, k):
        ind = bisect.bisect_left(self.popularities, k)
        if ind >= len(self.popularities):
            ind = len(self.popularities) - 1
        return self.popularities[ind]

    def sample(self, k):

        k1 = k

        if k not in self.samples_index:
            k = self.findnearest(k)

        curr_index = self.samples_index[k]
        if curr_index >= len(self.sampled_sizes[k]):
            self.sampled_sizes[k] = choices(self.pop_sz_vals[k], weights=self.pop_sz_prs[k], k=10000)
            self.samples_index[k] = 0
            curr_index = 0

        self.samples_index[k] += 1        
        return int(self.sampled_sizes[k][curr_index])
        #return (int(self.sampled_sizes[k][curr_index%50000])/10) + 1
                    
    #def sample_popularities(self, n):
        #return np.random.choice(self.popularities, n, p=self.popularities)
           

class pop:
    def __init__(self, i_file, min_val, max_val):
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

                if key > max_val:
                    break
                
            else:
                if key >= min_val:
                    sum_count += float(l[1])
                
                
            
        p_keys = list(self.popularities.keys())
        vals = []
        for k in p_keys:
            vals.append(self.popularities[k])

        sum_vals = sum(vals)
        vals = [float(x)/sum_vals for x in vals]

        print(p_keys, vals)
        
        self.p_keys = p_keys
        self.pr = vals

                
    def sample_popularities(self, n):
        return choices(self.p_keys, weights=self.pr,k=n)

            
            
class pop_opp:
    def __init__(self, i_file, min_val, max_val):
        f = open(i_file, "r")
        self.all_keys = defaultdict(int)

        l = f.readline()
        sum_count = 0

        total_pr = 0
        for l in f:
            l = l.strip().split(" ")

            if len(l) == 1:
                continue
            else:
                key = int(float(l[0]))
                val = float(l[1])
                if key >= min_val and key <= max_val:
                    self.all_keys[key] += val                                
                    total_pr += val
                    
        p_keys = list(self.all_keys.keys())
        vals = []
        for k in p_keys:
            vals.append(self.all_keys[k])

        sum_vals = sum(vals)
        vals = [float(x)/sum_vals for x in vals]
        
        self.p_keys = p_keys
        self.pr = vals

                
    def sample_keys(self, n):
        return choices(self.p_keys, weights=self.pr,k=n)

            
class pop_opp2:
    def __init__(self, i_file, min_val, max_val):
        f = open(i_file, "r")
        self.all_keys = defaultdict(int)

        l = f.readline()
        sum_count = 0

        total_pr = 0
        
        for l in f:
            l = l.strip().split(" ")

            if len(l) == 1:
                continue
            else:
                key = int(l[1])
                val = float(l[2])
                    
                if key >= min_val and key <= max_val: 
                    self.all_keys[key] += val
                    total_pr += val
            
        p_keys = list(self.all_keys.keys())
        vals = []
        for k in p_keys:
            vals.append(self.all_keys[k])

        sum_vals = sum(vals)
        vals = [float(x)/sum_vals for x in vals]
        
        self.p_keys = p_keys
        self.pr = vals

        print("total_pr : ", total_pr)
        print("pr[-200 : ", self.all_keys[-200])

        
    def sample_keys(self, n):
        return choices(self.p_keys, weights=self.pr,k=n)

        

class pop_opp3:
    def __init__(self, i_file, min_val, max_val):
        f = open(i_file, "r")
        self.all_keys = defaultdict(int)

        l = f.readline()
        sum_count = 0

        total_pr = 0
        for l in f:
            l = l.strip().split(" ")

            if len(l) == 1:
                continue
            else:
                key = int(float(l[0]))
                val = float(l[2])
                if key >= min_val and key <= max_val:
                    self.all_keys[key] += val                                
                    total_pr += val
                    
        p_keys = list(self.all_keys.keys())
        p_keys.sort()
        vals = []
        for k in p_keys:
            vals.append(self.all_keys[k])

        sum_vals = sum(vals)
        vals = [float(x)/sum_vals for x in vals]

        print(p_keys)
        print(vals)
        
        self.p_keys = p_keys
        self.pr = vals

                
    def sample_keys(self, n):
        return choices(self.p_keys, weights=self.pr,k=n)
        


            
        

    
