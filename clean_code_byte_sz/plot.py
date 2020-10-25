import matplotlib.pyplot as plt
from util import *
import sys

tc = sys.argv[1]

f = open("results/" + str(tc) + "//result_trace_fd_66_mil.txt", "r")
fds = []
prs = []
for l in f:
    l = l.strip().split(" ")
    fd = int(float(l[0]))
    pr = float(l[1])

    fds.append(fd)
    prs.append(pr)

    if fd > 800000000:
        break

max_pr = prs[-1]
scale = float(1)/max_pr
prs = [scale * x for x in prs]

plt.plot(fds, prs, label="result")


f = open("results/" + str(tc) + "/original_trace_fd.txt", "r")
fds = []
prs = []
for l in f:
    l = l.strip().split(" ")
    fd = int(l[0])
    pr = float(l[1])

    fds.append(fd)
    prs.append(pr)

    if fd > 800000000:
        break


max_pr = prs[-1]
scale = float(1)/max_pr
prs = [scale * x for x in prs]
plt.plot(fds, prs, label="original")

f = open("results/" + str(tc) + "/sampled_fds.txt", "r")
l = f.readline().strip().split(",")
l = l[:67108864]
l = [float(x) for x in l if float(x) < 800000000]

plot_list(l, label="sampled")
plt.xlabel("fds")
plt.ylabel("cdf")
plt.grid()
plt.legend()
plt.savefig("compare.png")
