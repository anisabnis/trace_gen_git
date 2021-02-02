import sys
from obj_size_dst import *
from obj_pop_dst import *
from joint_dst import *
from collections import defaultdict
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

def plot_list(x, label="-", maxlim=100000000000):
    a = defaultdict(int)
    for v in x:
        if v < maxlim:
            a[v] += 1

    plot_dict(a, label)

w_dir = sys.argv[1]

iat_dst = pop("results/" + w_dir + "/iat_pop_fnl.txt", 0, 39800)
prior_iats = iat_dst.sample_popularities(10*1000000)

iat_pop = pop_sz_dst("results/" + w_dir + "/iat_pop_fnl.txt", False, 39800, 0)
popularities = [iat_pop.sample(i) for i in prior_iats]

fd_sample = pop_sz_dst("results/" + w_dir + "/fd_final.txt") 

sampled_fds = []
for i, p in enumerate(popularities):
    for j in range(p):
        sampled_fds.append(fd_sample.sample(prior_iats[i]))

    if i %10000 == 0:
        print("completed objects : ", i)
        
plot_list(sampled_fds, "generated", 6000000000)

f = open("results/" + w_dir + "/fd_final.txt", "r")
l = f.readline()

fds = defaultdict(lambda : 0)
for l in f:
    l = l.strip().split(" ")
    fd = int(l[1])
    if fd < 6000000000:
        fds[fd] += float(l[2])

plot_dict(fds, "original")
plt.xlabel("FDS")
plt.ylabel("CDF")
plt.grid()
plt.legend()
plt.savefig("results/" + w_dir + "/fd.png")
plt.clf()

# f = open("results/" + w_dir + "/fd_final.txt", "r")
# l = f.readline()

# fds = defaultdict(lambda : 0)
# for l in f:
#     l = l.strip().split(" ")
#     iat = int(float(l[0]))
#     fds[iat] += float(l[2])

# plot_dict(fds, "original")
# plt.xlabel("IATS")
# plt.ylabel("CDF")
# plt.grid()
# plt.legend()
# plt.savefig("results/" + w_dir + "/iat.png")
# plt.clf()
