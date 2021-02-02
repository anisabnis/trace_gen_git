import sys
from parser import *
from util import *
from collections import defaultdict
import matplotlib.pyplot as plt

dir = sys.argv[1]

# f = open(dir + "/sampled_fds.txt", "r")
# l = f.readline()
# l = l.strip().split(",")
# #l = l[:50000000]
# fds = [int(x) for x in l if x!='']
# fds = [int(x) for x in fds if x < 6000000000]
# f.close()
# plot_list(fds, "generated")

f = open(dir + "/fd_final.txt", "r")
l = f.readline()

fds = defaultdict(lambda : 0)
for l in f:
    l = l.strip().split(" ")
    fd = int(l[1])
    fds[fd] += float(l[2])

plot_dict(fds, "original")
plt.xlabel("FDS")
plt.ylabel("CDF")
plt.grid()
plt.legend()
plt.savefig(dir + "/fd.png")
    





