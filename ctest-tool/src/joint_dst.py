from collections import defaultdict
#import matplotlib.pyplot as plt
from random import choices
from util import *
import numpy as np
import json
import bisect
import copy


class joint_dst:
    def __init__(self, i_file, opp=False, lowerlimit1=-1, lowerlimit2=-1):
        key_val = defaultdict(lambda : defaultdict(int))
        f = open(i_file, "r")
        f.readline()

        for l in f:
            l = l.strip().split(" ")

            key1 = int(float(l[0]))
            key2 = int(float(l[1]))
            val  = float(l[2])

            if opp == False:
                if key1 >= lowerlimit1 and key2 >= lowerlimit2:
                    key_val[key1][key2] += val
            else:
                if key2 >= lowerlimit1 and key1 >= lowerlimit2:
                    key_val[key2][key1] += val


        self.pop_sz_vals = defaultdict(lambda : list)
        self.pop_sz_prs = defaultdict(lambda : list)

        sum_n_key = 0

        for key in key_val:
            ## For each key1 what are the available key2s
            sizes = list(key_val[key].keys())
            n_key = key
            self.pop_sz_vals[n_key] = sizes

            ## For each key1 what is the probability of a key2
            prs = []
            for s in sizes:
                prs.append(key_val[key][s])
            sum_prs = sum(prs)
            prs = [float(x)/sum_prs for x in prs]
            self.pop_sz_prs[n_key] = prs

        self.sample_each_popularity()


    def sample_each_popularity(self):
        self.samples = defaultdict(list)
        self.sampled_sizes = defaultdict(list)

        for k in self.pop_sz_prs:
            self.sampled_sizes[k] = choices(self.pop_sz_vals[k], weights=self.pop_sz_prs[k], k=10000)

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

    

    
            

class pop_sz_dst:

    def __init__(self, i_file, opp=False, upperlimit= -1, lowerlimit = -1):
        upperlimit = -1

        pop_sz = defaultdict(lambda : defaultdict(int))        

        f = open(i_file, "r")

        tmp_file = i_file.split("/")[-1]
        
        if tmp_file == "footprint_desc_all.txt" or tmp_file == "popularity_sd_pop.txt":
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

            if tmp_file != "footprint_desc_all.txt" and tmp_file != "popularity_sd_pop.txt":
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

            if tmp_file == "footprint_desc_all.txt" or tmp_file == "popularity_sd_pop.txt":
                objs = float(l[2])
                sz   = int(float(l[1]))
            else:
                objs = float(l[1])
                sz   = int(float(l[0])) + 1
                
            if opp == False:
                if key >= lowerlimit:
                    pop_sz[key][sz] += objs
            else:
                if key >= lowerlimit:
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
        
        self.p_keys = p_keys
        self.pr = vals

                
    def sample_popularities(self, n):
        return choices(self.p_keys, weights=self.pr,k=n)

            
    def getPr(self, pp):
        i = 0
        while True:
            if self.p_keys[i] == pp:
                break
            i+=1
        return self.pr[i]

    
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
        

class byte_sd:
    def __init__(self, i_file, min_val, max_val):
        self.sd_keys = []
        self.sd_vals = []
        self.sd_frac = []
        self.orig_sd_vals = []
        self.sd_index = defaultdict(lambda : 0)
        self.zero_sds = 0        
        self.SD = defaultdict(lambda : 0)        

        f = open(i_file, "r")
        l = f.readline()
        l = l.strip().split(" ")
        bytes_miss = float(l[-1])
        bytes_req = float(l[1])
        self.bytes_req = bytes_req
        
        self.SD[-1] = float(bytes_miss)/bytes_req
        self.sd_index[-1] = 0

        for l in f:
            l = l.strip().split(" ")
            sd = int(l[1])
            self.SD[sd] += float(l[2])        

        self.sd_keys = list(self.SD.keys())
        self.sd_keys.sort()

        i = 1
        for sd in self.sd_keys:
            self.sd_vals.append(self.SD[sd])
            self.sd_index[sd] = i
            i += 1
            
        self.sd_frac = copy.deepcopy(self.sd_vals)
        self.orig_sd_vals = copy.deepcopy(self.sd_vals)

        self.total_bytes_req = 0
        
        
    def reset(self):
        self.sd_vals = self.orig_sd_vals
        self.sd_frac = self.orig_sd_vals
        self.total_bytes_req = 0
        
    def update(self, obj_sizes, sampled_sds):

        for i in range(len(obj_sizes)):
            fr = float(obj_sizes[i])/self.bytes_req
            ind = self.sd_index[sampled_sds[i]]

            self.total_bytes_req += obj_sizes[i]
            
            try:
                #self.sd_frac[ind] -= fr
                if self.sd_frac[ind] < 0:
                    self.sd_frac[ind] = 0
                    self.zero_sds += 1
            except:
                print("index : ", ind)
                    
        self.sd_vals = []
        sum_fr = sum(self.sd_frac)
        for fr in self.sd_frac:
            self.sd_vals.append(float(fr)/sum_fr)
                
        #if self.zero_sds >= len(self.sd_frac):
        if self.total_bytes_req >= self.bytes_req or self.zero_sds >= len(self.sd_frac): 
            self.reset()
            self.zero_sds = 0
            
    def sample_keys(self, obj_sizes, sampled_sds, n):
        self.update(obj_sizes, sampled_sds)
        return choices(self.sd_keys, weights = self.sd_vals, k = n)
    
