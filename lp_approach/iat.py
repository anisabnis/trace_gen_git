import sys
from util import *
import numpy as np
import bisect
import matplotlib.pyplot as plt
from collections import defaultdict


class iat:
    def __init__(self, fd):
        self.fd = fd
        
    def getIAT(self):
        ## Get IAT distribution from FD

        iats = self.fd.keys()
        iats.sort()
        pr = []

        for i in iats:
            p = sum([x[1] for x in self.fd[i]])
            pr.append(p)        

        return iats, pr


    def genTrace(self, no_objects, trace_len):
        ## Using IAT distribution generate a trace
        
        iats, pr = self.getIAT()
        pr = np.cumsum(pr)
        
        trace = []

        iat_distribution = []

        for i in range(no_objects):
            ts = sample(pr, iats)            
            bisect.insort(trace, [ts, i, 0])

            
        request_dst = defaultdict(int)


        for i in range(trace_len):
            ts = sample(pr, iats)
            curr_ts = trace[i][0]
            obj_id = trace[i][1]

            iat_distribution.append(ts)

            trace[i][2] = curr_ts + ts

            bisect.insort(trace, [curr_ts + ts, obj_id, 0])

            if i%1000 == 0:
                print("Reqests : ", i)

            request_dst[curr_ts + ts] += 1


        timestamps = request_dst.keys()
        timestamps.sort()
        requests = []
        for t in timestamps:
            requests.append(request_dst[t])
        requests = np.cumsum(requests)
        plt.plot(timestamps, requests)
        plt.savefig("req_dst.png")
        plt.clf()


        iat_distribution.sort()
        plt.plot(iat_distribution)
        plt.savefig("IAT.png")
        plt.clf()

        trace_lim = int(0.85 * len(trace))

        return trace[:trace_lim]
            

        
    
