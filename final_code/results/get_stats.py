import sys
import struct
from parser import *
from collections import defaultdict
from util import *

dir = sys.argv[1]
type = sys.argv[2]
bhr = sys.argv[3]

def req_sz_dst(reqs, sizes):
    reqs_sz_constructed = defaultdict(int)
    sz_dst = defaultdict(int)
    pop_dst = defaultdict(int)
    obj_seen = set()
    
    for r in reqs:
        sz = sizes[r]
        if r not in obj_seen:
            sz_dst[sz] += 1
            obj_seen.add(r)
        reqs_sz_constructed[sz] += 1
        pop_dst[r] += 1

    pop_count = defaultdict(int)
    for r in pop_dst:
        pop_count[pop_dst[r]] += 1
    
    return reqs_sz_constructed, sz_dst, pop_count

## For the constructed trace
if bhr == "b":
    f = open(dir + "/out_trace_" + str(type) + "_byte.txt", "r")
else:
    f = open(dir + "/out_trace_" + str(type) + "_byte.txt", "r")    
reqs = f.readline()
reqs = reqs.strip().split(",")[:-1]
reqs = reqs[50000000:]
reqs = [int(x) for x in reqs]
f.close()

if bhr == "b":
    f = open(dir + "/sampled_sizes_" + str(type) + "_byte.txt", "r")
else:
    f = open(dir + "/out_trace_" + str(type) + "_byte.txt", "r")    
sizes = f.readline()
sizes = sizes.strip()
sizes = [float(x) for x in sizes.split(",")]


req_sz, sz_dst, pop_dst = req_sz_dst(reqs, sizes)

if bhr == "b":
    f = open(dir + "/b_req_sz_dst.txt", "w")
else:
    f = open(dir + "/r_req_sz_dst.txt", "w")    
sz_keys = list(req_sz.keys())
sz_keys.sort()
for sz in sz_keys:
    f.write(str(sz) + " " + str(req_sz[sz]) + "\n")


if bhr == "b":
    f = open(dir + "/b_sz_dst.txt", "w")
else:
    f = open(dir + "/r_sz_dst.txt", "w")
sizes = list(sz_dst.keys())
sizes.sort()
for sz in sizes:
    f.write(str(sz) + " " + str(sz_dst[sz]) + "\n")

    
if bhr == "b":
    f = open(dir + "/b_pop_dst.txt", "w")
else:
    f = open(dir + "/r_pop_dst.txt", "w")
pops = list(pop_dst.keys())
pops.sort()
for p in pops:
    f.write(str(p) + " " + str(pop_dst[p]) + "\n")
    



    
