import numpy as np
import matplotlib.pyplot as plt

f = open("fd_bytes.txt", "r")
l = f.readline()

l = l.strip().split(" ")
key = int(l[0])

vals = []
prs = []

for l in f:
    l = l.strip().split(" ")
    if len(l) == 1:
        plt.clf()
        prs = np.cumsum(prs)
        plt.plot(vals, prs)
        plt.savefig("sd_pop/" + str(key) + ".png")
        key = int(l[0])
        vals = []
        prs = []
        continue


    vals.append(int(l[0]))
    prs.append(float(l[1]))
    

        
