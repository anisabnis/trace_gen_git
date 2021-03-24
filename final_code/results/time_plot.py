import numpy as np
import matplotlib.pyplot as plt

f = open("v/byte_sampled_fds.txt", "r")
l = f.readline()
l = l.strip().split(",")[:-1]
l = [int(x) for x in l]

i = 0
points = []
collected = []
for e in l:
    if i%100000 == 0:
        points.append(np.mean(collected))
        collected = []
    if e >= 0:
        collected.append(e)
    i += 1
    
plt.plot(points)
plt.savefig("v/time_plot.png")

