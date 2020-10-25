import matplotlib.pyplot as plt
from collections import defaultdict
import sys
import numpy as np

w_dir = sys.argv[1]
f = open("../" + w_dir + "/res_fd.txt")

fds = []
prs = []

for l in f:
    l = l.strip().split(" ")
    fds.append(int(l[0]))
    prs.append(float(l[1]))
fds = fds[:500000]
prs = prs[:500000]

f.close()

f = open("../" + w_dir + "/sampled_fds.txt")
l = f.readline()
l = l.split(",")
l = l[:-1]
l = [int(x) for x in l]

sd_dict = defaultdict(int)
for sd in l:
    sd_dict[sd] += 1

sd_keys = list(sd_dict.keys())
sd_keys.sort()
sd_vals = []
for sd in sd_keys:
    sd_vals.append(sd_dict[sd])

sum_sd_vals = sum(sd_vals)
sd_vals = [float(x)/sum_sd_vals for x in sd_vals]
sd_vals = np.cumsum(sd_vals)

sd_keys = sd_keys[:500000]
sd_vals = sd_vals[:500000]

plt.plot(fds, prs, label="alg", linestyle="-")
plt.plot(sd_keys, sd_vals, label="orig", linestyle="--")
plt.legend()
plt.grid()
plt.xlabel("Stack distance in KB")
plt.ylabel("CDF")
plt.savefig("../" + w_dir + "/StackDistance.png")
