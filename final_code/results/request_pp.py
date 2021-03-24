import sys
import struct
from parser import *
from collections import defaultdict
from util import *

MIL = 1000000

dir = sys.argv[1]
type = sys.argv[2]

def req_sz_dst(reqs, sizes):
    reqs_sz_constructed = defaultdict(int)
    for r in reqs:
        sz = sizes[r]
        reqs_sz_constructed[sz] += 1
    return reqs_sz_constructed


## For the constructed trace
f = open(dir + "/out_trace_" + str(type) + "_init.txt", "r")
reqs = f.readline()
reqs = reqs.strip().split(",")[:-1]
reqs = reqs[50*MIL:]
reqs = [int(x) for x in reqs]
f.close()

f = open(dir + "/sampled_pop_" + str(type) + "_init.txt", "r")
sizes = f.readline()
sizes = sizes.strip()
sizes = [float(x) for x in sizes.split(",")]
constructed = req_sz_dst(reqs, sizes)
plot_dict(constructed, "constructed")


## For the original trace
input = binaryParser(dir + "/akamai2.bin")
input.open()

sizes = defaultdict(lambda : 0)
reqs = []
i = 0
while True:
    try:
        r, sz, t = input.readline()
    except:
        break

    i += 1

    if i < 10*MIL:
        continue
    
    if r%8 != 0:
        continue

    sizes[r] += 1
    reqs.append(r)

    if i > 300*MIL:
        break

    
original = req_sz_dst(reqs, sizes)
plot_dict(original, "original")
plt.legend()
plt.grid()
plt.xlabel("Popularities")
plt.ylabel("CDF")
plt.xscale("log")
plt.savefig(dir + "/req_pop_" + str(type) + ".png")


    

