import json, sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import random
import os

w_dir = sys.argv[1]

with open("../" + w_dir + "/land_position.json", "r") as read_file:
    descrepency = json.load(read_file)

descrepency_ = defaultdict()
for d in descrepency:
    d1 = int(d.encode('ascii', 'ignore'))
    descrepency_[d1] = descrepency[d]

if not os.path.exists("../" + w_dir + "/fall"):
    os.mkdir("../" + w_dir + "/fall")

def plot_list(vals, label):
    a = defaultdict(int)
    for v in vals:
        a[v] += 1
    
    keys = a.keys()
    keys.sort()
    vals = []
    for k in keys:
        vals.append(a[k])

    s_vals = sum(vals)
    vals = [float(v)/s_vals for v in vals]
    vals = np.cumsum(vals)    

    plt.plot(keys, vals)
    plt.grid()
    plt.xlabel("fall position")
    plt.ylabel("probability")
    plt.title("size : " + str(label))
    plt.savefig("../" + w_dir + "/fall/" + str(label) + ".png")
    plt.clf()


f = open("../" + w_dir + "/sampled_sizes.txt")
l = f.readline()
l = l.strip().split(",")
l = [int(x) for x in l]

keys = descrepency_.keys()
for i in range(100):
    c_k = random.choice(keys)
    vals = descrepency_[c_k]
    vals = [float(x) for x in vals]    
    plot_list(vals, str(l[c_k]) + str(i))

