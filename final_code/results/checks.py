import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

d = sys.argv[1]

def plot_dict(x, label="-"):
    keys = list(x.keys())
    keys.sort()

    vals = []
    for k in keys:
        vals.append(x[k])
    
    sum_vals = sum(vals)
    vals = [float(x)/sum_vals for x in vals]
    vals = np.cumsum(vals)
    
    plt.plot(keys, vals, label=label)#, marker="^", markersize=3, markevery=500)


def plot_list(x, label="-", maxlim=100000000000):
    a = defaultdict(int)
    for v in x:
        if v < maxlim:
            a[v] += 1

    plot_dict(a, label)


f = open(d + "/sampled_fds.txt", "r")
l = f.readline()
l = l.strip().split(",")[:-1]
sampled_fds = [int(x) for x in l]

plot_list(sampled_fds)
plt.grid()
plt.xlabel("FDs")
plt.ylabel("CDF")
plt.savefig(d + "/sampled_fds.png")
