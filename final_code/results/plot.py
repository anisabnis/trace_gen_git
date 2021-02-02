import matplotlib.pyplot as plt
import numpy as np

f = open("v/footprint_desc_constructed_unit.txt","r")
xs = []
pr = []
for l in f:
    l = l.strip().split(" ")
    if l[0] == "-1":
        save = float(l[-1])
    else:
        xs.append(float(l[0]))
        pr.append(float(l[-1]))

xs.append(max(xs) + 200000)
pr.append(save)
pr = np.cumsum(pr)
plt.plot(xs, pr)
plt.grid()
plt.savefig("v/unit_fd.png")

