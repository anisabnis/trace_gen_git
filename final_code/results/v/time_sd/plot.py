import matplotlib.pyplot as plt
import numpy as np

i = 0
f = open("popularity_time_all.txt", "r")
for l in f:
    l = l.strip().split(",")
    if len(l) > 400:
        i += 1
        sds = [int(x) for x in l]
        sds = np.cumsum(sds)

        plt.plot(sds)
        plt.savefig("plots/" + str(i) + ".png")
        plt.grid()
        plt.clf()
        
