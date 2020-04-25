from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

f=open("st_out" ,"r")
f.readline()
sd = defaultdict(int)
for l in f:
    l = l.strip().split(" ")
    pr = float(l[2])
    s = int(l[1])
    sd[s] += pr

sds = list(sd.keys())
sds.sort()
sds_pr = []
for s in sds:
    sds_pr.append(sd[s])

sum_sds = sum(sds_pr)
sds_pr = [float(x)/sum_sds for x in sds_pr]
sds_pr = np.cumsum(sds_pr)

plt.plot(sds, sds_pr)
plt.savefig("fd_akamai.png")



    
    
