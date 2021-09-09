import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

TB = 1000000000

d = sys.argv[1]

def plot_dict(x, ohp, label="-"):
    print("ohp : ", ohp)

    #ohp = 0
    
    keys = list(x.keys())
    keys.sort()

    vals = []
    for k in keys:
        vals.append(x[k])

    # keys.append(keys[-1] + 200000)    
        
    sum_vals = sum(vals)
    vals = [float(y)/sum_vals for y in vals]    
    # vals = [(1-ohp)*y for y in vals]
    # vals.append(ohp)
    keys = keys[1:]
    vals = vals[1:]
    
    vals = np.cumsum(vals)
    
    plt.plot(keys, vals, label=label)#, marker="^", markersize=3, markevery=500)


def plot_list(x, ohp, label="-", maxlim=100*TB):
    a = defaultdict(int)
    for v in x:
        if v < maxlim:
            a[v] += 1

    plot_dict(a, ohp, label)

def plot_dict_2(x, ohp, label="-"):
    print("ohp : ", ohp)

    #ohp = 0
    
    keys = list(x.keys())
    keys.sort()

    vals = []
    for k in keys:
        vals.append(x[k])

    # keys.append(keys[-1] + 200000)    
        
    # vals = [(1-ohp)*y for y in vals]
    # vals.append(ohp)
    
    vals = np.cumsum(vals)
    
    plt.plot(keys, vals, label=label)#, marker="^", markersize=3, markevery=500)

    

def plot_orig(file_n):
    f = open(d + "/" + file_n, "r")
    #f = open(d + "/fd_final.txt", "r")
    #f = open(d + "/fd_final.txt", "r")
    l = f.readline()
    l = l.strip().split(" ")
    one_hits_pr = float(l[-2])/float(l[0])
    prs = defaultdict(lambda : 0)
    #prs[25*TB + 200000] += one_hits_pr

    total_pr = 0

    max_key = 0
    for l in f:
        l = l.strip().split(" ")
        key = int(l[1])
        pr = float(l[2])
        prs[key] += pr
        total_pr += pr
        if key > max_key:
            max_key = key

    #prs[-200000] += one_hits_pr
    plot_dict_2(prs, one_hits_pr, "original")

    print("total_pr : ", total_pr)
    return one_hits_pr, max_key

one_hit_pr, max_key = plot_orig("calculus_footprint_desc_mix.txt")
#one_hit_pr=0

#print(max_key)
f = open(d + "/sampled_fds_mix.txt", "r")
l = f.readline()
l = l.strip().split(",")[:-1]
sampled_fds = [int(x) for x in l]
print(max(sampled_fds))
#sampled_fds = [x for x in sampled_fds if x >= 0]
plot_list(sampled_fds, one_hit_pr, label="sampled")

# f = open("v/footprint_desc_constructed.txt","r")
# xs = []
# pr = []
# for l in f:
#     l = l.strip().split(" ")
#     if l[0] == "-1":
#         save = float(l[-1])
#     else:
#         xs.append(float(l[0]))
#         pr.append(float(l[-1]))

# xs.append(max(xs) + 200000)
# pr.append(save)
# pr = np.cumsum(pr)
# plt.plot(xs, pr, label="constructed")

plt.legend()
plt.grid()
plt.xlabel("FDs")
plt.ylabel("CDF")
plt.ylim(0,1)
plt.savefig(d + "/sampled_fds_mix.png")
