import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

TB = 1000000000

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


def plot_list(x, label="-", maxlim=100*TB):
    a = defaultdict(int)
    for v in x:
        if v < maxlim:
            a[v] += 1

    plot_dict(a, label)



f = open("v/generated_traces/out_trace_all.txt", "r")
l = f.readline()
l = l.strip().split(",")[:-1]
pops = [int(x) for x in l]
plot_list(pops, "popularity")
plt.legend()
plt.grid()
plt.savefig("v/popularities.png")
