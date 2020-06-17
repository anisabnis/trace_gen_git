import numpy as np
import json
from collections import defaultdict
from util import *
import matplotlib.pyplot as plt

class obj_size:
    def __init__(self, dir, o_file):
        with open(dir + "/" + o_file, "r") as read_file:
            size_dst = json.load(read_file)

        sizes = list(size_dst.keys())
        sizes = [int(x.encode("utf-8")) for x in sizes]
        sizes.sort()        

        req_sizes = defaultdict(int)
        for s in sizes:
            sz = int(s)
            s = unicode(str(s), "utf-8")
            count = size_dst[s]
            req_sizes[sz] += count
            
        sizes = []
        size_prs = []
        req_sizes_keys = list(req_sizes)
        req_sizes_keys.sort()
        for s in req_sizes_keys:
            if s > 0:
                sizes.append(s)
                size_prs.append(req_sizes[s])

        sum_pr = sum(size_prs)
        size_prs = [float(p)/sum_pr for p in size_prs]
        self.size_dst = size_prs
        self.size_prs = np.cumsum(size_prs)
        self.sizes = sizes

        plt.plot(self.sizes, self.size_prs, label="distribution")

    def get_objects(self, no_objects):
        return np.random.choice(self.sizes, no_objects, p=self.size_dst)
