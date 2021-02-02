import sys
import matplotlib.pyplot as plt
import numpy as np
from util import *

f = open("sampled_fds_2.txt" ,"r")
l = f.readline()
l = l.split(",")
l = [int(x) for x in l]
plot_list(l, label="generated")
f.close()

f = open("original_2.txt" , "r")
fds = []
prs = []
for l in f:
    l = l.strip().split(" ")
    fd = int(l[0])
    fd = fd/1000
    pr = float(l[1])

    fds.append(fd)
    prs.append(pr)

#sum_prs = sum(prs)
#prs = [float(x)/sum_prs for x in prs]
#prs = np.cumsum(prs)

plt.plot(fds, prs, label="original")
plt.legend()
plt.grid()
plt.savefig("fds_2.png")



