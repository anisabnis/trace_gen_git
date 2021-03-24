import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

TB = 1000000000

d = sys.argv[1]

def plot_dict(x, ohp, label="-",marker="^"):
    print("ohp : ", ohp)

    keys = list(x.keys())
    keys.sort()

    ## remove this line
    #ohp = 0

    vals = []
    for k in keys:
        vals.append(x[k])

    keys.append(keys[-1] + 200000)    

    
    sum_vals = sum(vals)
    vals = [float(y)/sum_vals for y in vals]
    vals = [(1-ohp)*y for y in vals]
    vals.append(ohp)
    
    vals = np.cumsum(vals)
    
    plt.plot(keys, vals, label=label)#, marker=marker, markevery=5000)#, marker="^", markersize=3, markevery=500)


def plot_list(x, ohp, label="-", marker="^", maxlim=100*TB):
    a = defaultdict(int)
    for v in x:
        if v < maxlim:
            a[v] += 1

    plot_dict(a, ohp, label, marker)


def plot_orig():
    f = open(d + "/pop_sd_0.txt", "r")
    #f = open(d + "/fd_final.txt", "r")
    #f = open(d + "/fd_final.txt", "r")
    l = f.readline()
    l = l.strip().split(" ")
    one_hits_pr = float(l[-1])/float(l[0])
    prs = defaultdict(lambda : 0)
    #prs[25*TB + 200000] += one_hits_pr

    total_pr = 0

    max_key = 0
    for l in f:
        l = l.strip().split(" ")
        key = int(l[1])
        pr = float(l[2])
        #if key <= 1:
            #pass
        #    one_hits_pr += pr
        #else:
        prs[key] += pr
        total_pr += pr

        if key > max_key:
            max_key = key

    #prs[max_key + 200000] += one_hits_pr
    plot_dict(prs, one_hits_pr, "original", "^")

    print("total_pr : ", total_pr, one_hits_pr)
    return one_hits_pr
    
one_hit_pr = plot_orig()
    
# f = open("v/footprint_desc_constructed_pop.txt","r")
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
# #pr.append(one_hit_pr)
# pr.append(save)
# pr = np.cumsum(pr)
# plt.plot(xs, pr, label="constructed")

#Find fraction of requests which were for one hits
# total_reqs = 0
# obj_reqs = defaultdict(lambda : 0)
# f = open(d + "/out_trace_pop_init.txt")
# l = f.readline()
# l = l.strip().split(",")[:-1]
# l = l[50000000:]
# print(len(l))
# for r in l:
#     obj_reqs[r] += 1
#     total_reqs += 1
# counter = 0
# for o in obj_reqs:
#     if obj_reqs[o] == 1:
#         counter += 1
# save = float(counter)/total_reqs
# print("result ohp : ", save)
#### 
save = 0
f = open(d + "/sampled_fds_pop_init.txt", "r")
l = f.readline()
l = l.strip().split(",")[:-1]
sampled_fds = [int(x) for x in l]
sampled_fds = sampled_fds[50000000:]
plot_list(sampled_fds, save, label="sampled",marker="x")


plt.legend()
plt.grid()
plt.xlabel("FDs")
plt.ylabel("CDF")
plt.savefig(d + "/sampled_fds_pop_init.png")
