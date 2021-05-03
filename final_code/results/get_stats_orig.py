import sys
import struct
from parser import *
from collections import defaultdict
from util import *

dir = sys.argv[1]

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


if dir == "v":
    input = binaryParser(dir + "/akamai2.bin")
elif dir == "w":
    input = binaryParser(dir + "/akamai1.bin")
elif dir == "tc":
    input = allParser(dir + "/all.gz")
elif dir == "eu":
    input = euParser(dir + "/all_sort_int")
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

    if i % 100000 == 0:
        print("lines ", i)
    sizes[r] = max(1, int(sz)/1000)
    reqs.append(r)

    if i > 200000000:
        break

req_sz, sz_dst, pop_dst = req_sz_dst(reqs, sizes)

f = open(dir + "/req_sz_dst.txt", "w")
sz_keys = list(req_sz.keys())
sz_keys.sort()
for sz in sz_keys:
    f.write(str(sz) + " " + str(req_sz[sz]) + "\n")


f = open(dir + "/sz_dst.txt", "w")
sizes = list(sz_dst.keys())
sizes.sort()
for sz in sizes:
    f.write(str(sz) + " " + str(sz_dst[sz]) + "\n")

    
f = open(dir + "/pop_dst.txt", "w")
pops = list(pop_dst.keys())
pops.sort()
for p in pops:
    f.write(str(p) + " " + str(pop_dst[p]) + "\n")
    



    
