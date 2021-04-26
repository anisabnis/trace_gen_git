f = open("test.txt", "r")
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

def plot_list(x, label="-", maxlim=100000000000):
    a = defaultdict(int)
    for v in x:
        if v < maxlim:
            a[v] += 1

    plot_dict(a, label)
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


sds = []
for l in f:
    l = l.strip().split(" ")
    sd = int(l[1])
    sds.append(sd)

plot_list(sds, "sample")

f.close()
f = open("results/v/popularity_desc_all.txt", "r")
prs = {}
for l in f:
    l = l.strip().split(" ")
    p = int(l[0])
    if p == 130:
        prs[int(l[1])] = float(l[2])

plot_dict(prs)
plt.grid()
plt.legend()
plt.savefig("test.png")
    
