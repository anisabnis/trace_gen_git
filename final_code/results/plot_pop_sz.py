import sys
import matplotlib.pyplot as plt
from collections import defaultdict

d = sys.argv[1]
f = open(str(d) + "/joint_dst.txt", "r")
l = f.readline()

p = int(l.strip())
prs = defaultdict(int)

for l in f:
    l = l.strip().split(" ")

    if len(l) == 1:
        keys = prs.keys()
        keys.sort()
        vals = []

        for k in keys:
            vals.append(prs[k])

        plt.clf()
        plt.plot(keys, vals)
        plt.xlabel("size (KB)")
        plt.savefig(str(d) + "/sz_dst/" + str(p) + ".png")

        prs = defaultdict()
        p = int(l[0])
        
    else:
        k = int(float(l[0]))
        v = float(l[1])
        prs[k] = v
