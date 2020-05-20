import matplotlib.pyplot as plt
from util import *
f = open("sampled_sizes.txt", "r")
sizes = []
for l in f:
    l = l.strip()
    sz = int(l)
    sizes.append(sz)
sizes.sort()
plot_list(sizes[:len(sizes)/2])
plt.savefig("sampled_sz.png")
