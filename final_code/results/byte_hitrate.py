import matplotlib.pyplot as plt
import sys

dir = sys.argv[1]
MIL = 1000000
cs = int(sys.argv[2]) * MIL

def hitrate(fname):
    f = open(dir + "/simulations/" + fname, "r")
    bytes_req = 0
    lru_hit = 0
    stat = []    
    for l in f:
        try:
            l = l.strip().split(" ")
            lru_hit += int(l[-2])
            bytes_req += int(l[0])
            r = float(lru_hit)/bytes_req
            stat.append(r)
        except:
            continue
        
    return stat


orig = hitrate("original.stats_500000000.txt")
print(orig)
#orig = hitrate("original.stats" + str(cs) + "_0.txt")
#new = hitrate("generated.stats" + str(cs) + ".txt")
#lrusm = hitrate("generated.stats_lrusm" + str(cs) + ".txt")
#sz  = hitrate("generated.stats" + str(cs) + "_sz.txt")

plt.plot(orig, marker="x", markevery=10000,label="original")
#plt.plot(sz, marker="x", markevery=10000,label="size-sd")

#plt.plot(new, marker="o", markevery=10000, label="OurMethod")
#plt.plot(lrusm, marker="^", markevery=10000, label="Lrusm")
plt.xlabel("requests")
plt.ylabel("hitrate")
plt.legend()
plt.grid()
plt.title("Byte Hitrate")
plt.savefig(dir + "/byte_hitrate_sz_sd_" + str(cs) + ".png")
