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

def req_pop_dst(reqs):
    obj_reqs = defaultdict(lambda : 0)
    for r in reqs:
        obj_reqs[r] += 1
    req_obj = defaultdict(int)
    for o in obj_reqs:
        req_obj[obj_reqs[o]] += 1
    return req_obj

## For the constructed trace
f = open(dir + "/out_trace_" + str(type) + "_init.txt", "r")
reqs = f.readline()
reqs = reqs.strip().split(",")[:-1]
reqs = [int(x) for x in reqs]
f.close()
constructed = req_pop_dst(reqs)

c_keys = list(constructed.keys())
c_keys.sort()
c_vals = []
for ck in c_keys:
    c_vals.append(constructed[ck])
sum_vals = sum(c_vals)
f = open(dir + "/test_constructed.txt", "w")
for i in range(len(c_keys)):
    f.write(str(c_keys[i]) + " " + str(c_vals[i]) + "\n")
f.close()

    
#print(constructed)
#plot_dict(constructed, "constructed")

#For the original trace
input = binaryParser(dir + "/akamai2.bin")
input.open()
reqs = []
i = 0
while True:
    try:
        r, sz, t = input.readline()
    except:
        break        

    i  += 1
    if r%8 != 0:
        continue
    reqs.append(r)

    if i > 300000000:
        break
    
original = req_pop_dst(reqs)
c_keys = list(original.keys())
c_keys.sort()
c_vals = []
for ck in c_keys:
    c_vals.append(original[ck])
sum_vals = sum(c_vals)
f = open(dir + "/test_original.txt", "w")
for i in range(len(c_keys)):
    f.write(str(c_keys[i]) + " " + str(c_vals[i]) + "\n")
f.close()


print(original)
plot_dict(original, "original")
plt.legend()
plt.grid()
plt.xlabel("Popularities")
plt.ylabel("CDF of Objects")
plt.savefig(dir + "/req_pop_" + str(type) + ".png")


    

