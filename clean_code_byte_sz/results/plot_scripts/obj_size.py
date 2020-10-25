import sys
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

w_dir = sys.argv[1]
f = open("../" + w_dir + "/sampled_sizes.txt", "r")
l = f.readline().split(",")
l = [int(x) for x in l]

avg_size = sum(l)/len(l)
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

print("len", len(sd_keys))

sd_keys = sd_keys
sd_vals = sd_vals

plt.plot(sd_keys, sd_vals)
plt.legend()
plt.grid()
plt.xlabel("Obj size")
plt.ylabel("CDF")
plt.savefig("../" + w_dir + "/size_dst.png")

print("avg size : ", avg_size, len(l))
