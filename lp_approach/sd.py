import sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

class sd:
    def __init__(self, fd):
        self.fd = fd

    def getExpectedSDForT(self, t):
        req_fd = self.fd[t]
        return sum([req_fd[i][0] * req_fd[i][1] for i in range(len(req_fd))])

    def getSDDist(self, t):
        return self.fd[t]

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
