from collections import defaultdict
import random
import numpy as np
import copy

def gen_fd2(trace):
    fd_d = defaultdict(lambda : 0)
    counter = 0
    sc = 100

    for i in range(len(trace)):        
        if i%1000 == 0:
            print("generating fd : ", i)

        uniq_bytes = 0
        curr_item = trace[i][1]
        uniq_objects = set()
        success = False

        for k in range(i + 1, len(trace)):
            if trace[k][1] == curr_item:
                #uniq_bytes += sizes[curr_item]
                success = True
                break
            else:
                if trace[k][1] not in uniq_objects:
                    uniq_bytes += trace[k][2]
                    uniq_objects.add(trace[k][1])
             

        if success == True:
            key =  int(float(uniq_bytes)/sc) * sc
            fd_d[key] += 1
        else:
            counter += 1


    ks = list(fd_d.keys())
    ks.sort()

    counts = []
    for k in ks:
        counts.append(fd_d[k])
        
    sum_counts = sum(counts)
    counts = [float(x)/sum_counts for x in counts]
    
    s_counts = copy.deepcopy(counts)
    
    counts = np.cumsum(counts)
    return counts, s_counts, ks


class traceProp:
    def __init__(self, f):
        self.f = f
        ## Compute everything here
        ## fd, size dist, pop dist
        f = open("data_30/sub_trace.txt", "r")
        trace = []
        sz_dst = defaultdict(int)
        pop_dst = defaultdict(int)
        obj_sizes = defaultdict(int)

        i = 0
        for l in f:
#            if i == 10000:
#                break
            l = l.strip().split(" ")
            l = [int(x) for x in l]
            sz = np.ceil(float(l[2])/1000)
            oid = l[1]
            sz_dst[sz] += 1
            pop_dst[oid] += 1
            obj_sizes[oid] = sz
            trace.append(l)
            i = i+1

        self.fd, self.sfd1, self.sds1 = gen_fd2(trace)

        oids = list(pop_dst.keys())
        oids.sort()
        
        sizes = []
        popularities = []
        for o in oids:
            sizes.append(obj_sizes[o])
            popularities.append(pop_dst[o])

        sum_p = sum(popularities)
        popularities = [float(x)/sum_p for x in popularities]
        self.pop = popularities
        popularities = np.cumsum(popularities)
        
        self.sizes = sizes
        self.popularities = popularities
        self.trace_len = len(trace)


    def sample(self):
        z = np.random.random()

        obj = len(self.popularities) - 1
        pr = 0

        for i in range(len(self.popularities)):            
            if self.popularities[i] > z:
                obj = i
                break
        return obj


    def get_objects(self):
        return self.sizes, self.popularities

    def get_sd(self):
        return self.fd, self.sfd1, self.sds1

    def get_random_trace(self):
        trace = []
        for i in range(self.trace_len):
            req = self.sample()
            trace.append(req)
        return trace
        


    def getDelta(self,objects,min_obj_sz, max_obj_sz, scale):
        probabilities = []
        d_vals = []

        #for d in range(min_fd, max_fd+1):
        init_val = min_obj_sz
        while init_val < max_obj_sz:
            prob = 0
            d = init_val
            for i in range(len(objects)):
                sz = objects[i]
                p = self.pop[i]                
                if sz > abs(d):
                    prob += (p * sz) * (float(1)/(1 + sz)) * (1 - float(abs(d))/sz)
        
            probabilities.append(prob)
            d_vals.append(d)
            init_val += scale

        sum_p = sum(probabilities)
        print("sum _p ", sum_p)
        probabilities = [(float(p)/sum_p) for p in probabilities]
        
        probabilities_sum = np.cumsum(probabilities)

        return probabilities_sum, d_vals, probabilities
        
