import matplotlib.pyplot as plt
import sys

dir = sys.argv[1]
MIL = 1000000
cs = int(sys.argv[2]) * MIL

def hitrate(fname):
    f = open(dir + "/" + fname, "r")
    bytes_req = 0
    lru_hit = 0
    stat = []
    for l in f:
        l = l.strip().split(" ")
        lru_hit += int(l[-2])
        bytes_req += int(l[0])
        r = float(lru_hit)/bytes_req
        stat.append(r)
        
    return stat

orig = hitrate("original.stats" + str(cs) + "_0.txt")
#new = hitrate("generated.stats" + str(cs) + ".txt")
#lrusm = hitrate("generated.stats_lrusm" + str(cs) + ".txt")
sz  = hitrate("generated.stats" + str(cs) + "_pop.txt")

plt.plot(orig, marker="x", markevery=10000,label="original")
#plt.plot(new, marker="o", markevery=10000,label="OurMethod")
#plt.plot(lrusm, marker="^", markevery=10000,label="Lrusm")
plt.plot(sz, marker="x", markevery=10000,label="Pop")
plt.xlabel("requests")
plt.ylabel("hitrate")
plt.legend()
plt.grid()
plt.title("Object Hitrate")
plt.savefig(dir + "/obj_hitrate.png")
