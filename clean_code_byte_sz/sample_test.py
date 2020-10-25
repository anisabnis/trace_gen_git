f = open("results/4/fd_bytes.txt")
#l = f.readline()
from util import *
import matplotlib.pyplot as plt
import numpy as np

#key = int(l.strip().split(" ")[0])
save = False
fds = []
prs = []
for l in f:
    l = l.strip().split(" ")
    if len(l) == 1:
        key = int(l[0])
        if save == True:
            break
        if key == 512:
            save = True
        continue

    if save == True:
        fds.append(int(l[0]))
        prs.append(float(l[1]))

prs = np.cumsum(prs)
plt.plot(fds, prs)
plt.savefig("samplee.png")
        
