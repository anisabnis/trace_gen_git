import numpy as np
import matplotlib.pyplot as plt

f = open("cache_state_0_8.txt", "r")
sizes = []
popularities = []
for l in f:
    l = l.strip().split(",")
    sizes.append(float(l[2]))
    popularities.append(int(l[1]))

ttl_sz = sum(sizes)
ttl_pp = sum(popularities)

sizes = [float(x)/ttl_sz for x in sizes]
sizes = np.cumsum(sizes)

popularities = [float(x)/ttl_pp for x in popularities]
popularities = np.cumsum(popularities)

plt.plot(sizes)
plt.savefig("cache_state_sz.png")
plt.clf()

plt.plot(popularities)
plt.savefig("cache_state_pop.png")


