import json
from collections import defaultdict
import numpy as np
import random
import copy

class obj_size:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.sz_dst = json.load(f)
                    
        self.n_sz_dst = defaultdict(lambda : 0)
        self.obj_sizes = []

        for k in self.sz_dst:
            k1 = int(k.decode())
            k1 = k1/30000000
            self.n_sz_dst[k1] += int(self.sz_dst[k])

        self.obj_sizes = list(self.n_sz_dst.keys())
        self.obj_sizes.sort()
        self.obj_size_cnts = []

        for o in self.obj_sizes:
            self.obj_size_cnts.append(self.n_sz_dst[o])

        footprint = sum(self.obj_sizes)

        self.obj_size_cnts = [float(x)/footprint for x in self.obj_sizes]
        self.obj_size_cnts = np.cumsum(self.obj_size_cnts)


    def sample(self):
        z = np.random.random()

        sz = self.obj_sizes[-1]
        pr = 0

        for i in range(len(self.obj_size_cnts)):            
            if self.obj_size_cnts[i] > z:
                sz, pr = self.obj_sizes[i], (self.obj_size_cnts[i] - self.obj_size_cnts[i-1])
                break

        return sz, pr


class obj_size_uniform:
    def __init__(self, min_sz, max_sz):
        self.min_sz = min_sz
        self.max_sz = max_sz

    def get_objects(self, no_obj):        

        obj_sz = []
        obj_size_dst = defaultdict(lambda : 0)        

        for i in range(no_obj):
            sz = random.randint(self.min_sz, self.max_sz)
            obj_sz.append(sz)
            obj_size_dst[sz] += 1

        obj_sizes = list(obj_size_dst.keys())
        obj_sizes.sort()
        dst = []

        for sz in obj_sizes:
            dst.append(obj_size_dst[sz])
            
        sum_dst = sum(dst)
        
        dst = [float(x)/sum_dst for x in dst]

        return obj_sz, dst


class obj_size_two_distribution:
    def __init__(self, r1_min, r1_max, r2_min, r2_max, p1):
        self.r1_min = r1_min
        self.r1_max = r1_max
        self.r2_min = r2_min
        self.r2_max = r2_max
        self.p = p1

    def get_objects(self, no_obj):
        
        obj_sz = []
        obj_size_dst = defaultdict(lambda : 0)        

        no_obj1 = int(self.p * no_obj)

        for i in range(no_obj1):
            sz = random.randint(self.r1_min, self.r1_max)
            obj_sz.append(sz)
            obj_size_dst[sz] += 1

        no_obj2 = int((1 - self.p)*no_obj)
        for i in range(no_obj2):
            sz = random.randint(self.r2_min, self.r2_max)
            obj_sz.append(sz)
            obj_size_dst[sz] += 1

        obj_sizes = list(obj_size_dst.keys())
        obj_sizes.sort()
        dst = []

        for sz in obj_sizes:
            dst.append(obj_size_dst[sz])
            
        sum_dst = sum(dst)
        
        dst = [float(x)/sum_dst for x in dst]

        return obj_sz, dst



class obj_size_three_distribution:
    def __init__(self, r1_min, r1_max, r2_min, r2_max, r3_min, r3_max, p1, p2, p3):
        self.r1_min = r1_min
        self.r1_max = r1_max
        self.r2_min = r2_min
        self.r2_max = r2_max
        self.r3_min = r3_min
        self.r3_max = r3_max
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def get_objects(self, no_obj):
        
        obj_sz = []
        obj_size_dst = defaultdict(lambda : 0)        

        no_obj1 = int(self.p1 * no_obj)
        no_obj2 = int(self.p2 * no_obj)
        no_obj3 = int(self.p3 * no_obj)

        for i in range(no_obj1):
            sz = random.randint(self.r1_min, self.r1_max)
            obj_sz.append(sz)
            obj_size_dst[sz] += 1

        for i in range(no_obj2):
            sz = random.randint(self.r2_min, self.r2_max)
            obj_sz.append(sz)
            obj_size_dst[sz] += 1

        for i in range(no_obj3):
            sz = random.randint(self.r3_min, self.r3_max)
            obj_sz.append(sz)
            obj_size_dst[sz] += 1

        random.shuffle(obj_sz)

        obj_sizes = list(obj_size_dst.keys())
        obj_sizes.sort()
        dst = []

        for sz in obj_sizes:
            dst.append(obj_size_dst[sz])
            
        sum_dst = sum(dst)
        
        dst = [float(x)/sum_dst for x in dst]

        return obj_sz, dst






