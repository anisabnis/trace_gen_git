from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt


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


def save_dict(x, f):
    keys = list(x.keys())
    keys.sort()

    vals = []
    for k in keys:
        vals.append(x[k])
    
    sum_vals = sum(vals)
    vals = [float(x)/sum_vals for x in vals]
    vals = np.cumsum(vals)
    i = 0
    for k in keys:
        f.write(str(k) + " " + str(vals[i]) + "\n")


def save_list(x, f):
    a = defaultdict(int)
    for v in x:
        a[v] += 1
    save_dict(a, f)
    

def plot_list(x, label="-", maxlim=100000000000):
    a = defaultdict(int)
    for v in x:
        if v < maxlim:
            a[v] += 1

    plot_dict(a, label)
