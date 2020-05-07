import numpy as np
import json

class obj_size:
    def __init__(self, dir, o_file):
        with open(dir + "/" + o_file, "r") as read_file:
            size_dst = json.load(read_file)

        sizes = list(size_dst.keys())
        sizes = [int(x.encode("utf-8")) for x in sizes]
        sizes.sort()

        size_prs = []
        for s in sizes:
            s = unicode(str(s), "utf-8")
            size_prs.append(size_dst[s])
            
        sum_pr = sum(size_prs)
        size_prs = [float(p)/sum_pr for p in size_prs]
        size_prs = np.cumsum(size_prs)

        self.sizes = sizes
        self.size_prs = np.cumsum(size_prs)

    def sample(self):
        z = np.random.random()
        obj = self.sizes[-1]
        for i in range(len(self.sizes)):
            if self.size_prs[i] >= z:
                obj = self.sizes[i]
                break
        return obj

    def get_objects(self, no_objects):
        self.objects = []
        for i in range(no_objects):
            sz = self.sample()
            self.objects.append(sz)
