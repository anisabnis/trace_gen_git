import matplotlib.pyplot as plt
import numpy as np
f = open("test_constructed_new.txt", "r")
keys = []
vals = []
for l in f:
    l = l.strip().split(" ")
    keys.append(int(l[0]))
    vals.append(float(l[1]))
vals = np.cumsum(vals)
plt.plot(keys, vals, label="constructed")

keys = []
vals = []
f = open("test_original_new.txt", "r")
for l in f:
    l = l.strip().split(" ")
    keys.append(int(l[0]))
    vals.append(float(l[1]))
vals = np.cumsum(vals)
plt.plot(keys, vals, label="original")
plt.xlabel("popularities")
plt.grid()
plt.legend()
plt.ylabel("CDF")
plt.xscale("log")
plt.savefig("parse.png")
