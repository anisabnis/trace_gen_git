import sys
import matplotlib.pyplot as plt
from joint_dst import *
from util import *
import numpy as np

TB = 1000000000
MIL = 1000000
w_dir = sys.argv[1]

pop_dst = pop("results/" + w_dir + "/joint_dst_0.txt", 0, MIL)
popularities = pop_dst.sample_popularities(50*MIL)

plot_list(popularities, "sampled")
pl = np.cumsum(pop_dst.pr)
plt.plot(pop_dst.p_keys, pl, label="orig")
plt.grid()
plt.xlabel("popularities")
plt.legend()
plt.ylabel("cdf")
plt.xscale("log")
plt.savefig("results/v/popularity_sanity.png")
plt.clf()

sz_dst = pop_opp("results/" + w_dir + "/joint_dst_0.txt", 0 , TB)
pop_sz = pop_sz_dst("results/" + w_dir + "/joint_dst_0.txt")
pl = np.cumsum(sz_dst.pr)
plt.plot(sz_dst.p_keys, pl, label="orig")
i = 0
total_sz = 0
sizes = []
for p in popularities:
    sz = pop_sz.sample(p)
    sizes.append(sz)
    
plot_list(sizes, label="sampled")
plt.xlabel("sizes")
plt.legend()
plt.ylabel("cdf")
plt.xscale("log")
plt.grid()
plt.savefig("results/v/size_sanity.png")

plt.clf()
pp = 2
fd_sample = joint_dst("results/" + w_dir + "/pop_sd_0.txt", False, 2)
fds = []
for i in range(MIL):
    fds.append(fd_sample.sample(pp))

plot_list(fds, label="sampled")
keys = fd_sample.pop_sz_vals[pp]
vals = fd_sample.pop_sz_prs[pp]
vals = np.cumsum(vals)
plt.plot(keys, vals, label="orig")
plt.savefig("results/v/2.png")
