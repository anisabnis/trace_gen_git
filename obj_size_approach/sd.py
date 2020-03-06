import sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

class sd:
    def __init__(self, fd):
        self.fd = fd
        self.sd_dst = defaultdict(lambda : 0)
        
        for t in self.fd:
            for s in self.fd[t]:
                self.sd_dst[s[0]] += s[1]
        

        self.sds = list(self.sd_dst.keys())
        self.sds.sort()
        self.sds_pr = []

        for s in self.sds:
            self.sds_pr.append(self.sd_dst[s])

        sum_prs = sum(self.sds_pr)

        self.sds_pr = [float(x)/sum_prs for x in self.sds_pr]
        self.sds_pr = np.cumsum(self.sds_pr)


    def getExpectedSDForT(self, t):
        req_fd = self.fd[t]
        return sum([req_fd[i][0] * req_fd[i][1] for i in range(len(req_fd))])

    def getSDDist(self, t):
        return self.fd[t]


    def sampleSD(self):
        z = np.random.random()
        sd = self.sds[-1]

        for i in range(len(self.sds_pr)):
            if self.sds_pr[i] > z:
                sd = self.sds[i]
                break
        return sd

    def getSDDistGaussian(self, t):
        try:
            sd = self.fd[t][0]
            sd = sd[0]        
            #fd = np.random.normal(sd, 0.1 * sd, 1)[0]
            return sd
        except:
            print("debug : ", self.fd[t])
            return -1

    def getSDDist(self, t):
        ## Fix this
        pass

    def assignSD(self, trace):
        SDS = []

        for i in range(len(trace)):
            if trace[i][2] <= 0:
                continue

            diff = trace[i][2] - trace[i][0]
            sd = self.getSDDistGaussian(diff)
            trace[i].append(sd)
            SDS.append(sd)

        SDS.sort()
        plt.clf()
        plt.plot(SDS)
        plt.savefig("SDS.png")
