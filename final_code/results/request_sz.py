import sys
import struct
from parser import *
from collections import defaultdict
from util import *

dir = sys.argv[1]
type = sys.argv[2]

def req_sz_dst(reqs, sizes):
    reqs_sz_constructed = defaultdict(int)
    for r in reqs:
        sz = sizes[r]
        reqs_sz_constructed[sz] += 1
    return reqs_sz_constructed


## For the constructed trace
f = open(dir + "/out_trace_" + str(type) + ".txt", "r")
reqs = f.readline()
reqs = reqs.strip().split(",")[:-1]
reqs = reqs[100000000:]
reqs = [int(x) for x in reqs]
f.close()

f = open(dir + "/sampled_sizes_" + str(type) + ".txt", "r")
sizes = f.readline()
sizes = sizes.strip()
sizes = [float(x) for x in sizes.split(",")]
constructed = req_sz_dst(reqs, sizes)
plot_dict(constructed, "constructed")


## For the original trace
#input = binaryParser(dir + "/akamai1.bin")
#input.open()
input = allParser(dir + "/all.gz")
input.open()
sizes = defaultdict()
reqs = []
i = 0
while True:
    i += 1
    try:
        r, sz, t = input.readline()
    except:
        break
        
    # if r%8 != 0:
    #     continue
    sizes[r] = int(sz)/1000
    reqs.append(r)

    if i > 100000000:
        break
    
original = req_sz_dst(reqs, sizes)
plot_dict(original, "original")
plt.legend()
plt.grid()
plt.xlabel("sizes")
plt.xscale("log")
plt.ylabel("CDF")
plt.savefig(dir + "/req_sz_" + str(type) + ".png")


    

