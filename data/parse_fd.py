import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

class FD:
    def __init__(self, dir, fd_file):
        f = open(dir + "/" + fd_file, "r")
        f.readline()
        sd = defaultdict(int)
        for l in f:
            l = l.strip().split(" ")
            pr = float(l[1])
            s = int(l[0])
            sd[s] += pr

        sds = list(sd.keys())
        sds.sort()
        sds_pr = []
        for s in sds:
            sds_pr.append(sd[s])
            
        sum_sds = sum(sds_pr)
        sds_pr = [float(x)/sum_sds for x in sds_pr]
        self.sds_pdf = sds_pr

        sds_pr = np.cumsum(sds_pr)

        self.sds = sds
        self.sds_pr = sds_pr

        plt.plot(self.sds, self.sds_pr)


    def sample(self):
        z = np.random.random()
        obj = self.sds[-1]
        for i in range(len(self.sds)):
            if self.sds_pr[i] >= z:
                obj = self.sds[i]
                break

        return obj











