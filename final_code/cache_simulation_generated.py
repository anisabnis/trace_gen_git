import sys
from lru import *
from fifo import *
from util import *
from parser import *
import random

tc = sys.argv[1]
cache_size = int(sys.argv[2]) * 1000000
ignore = int(sys.argv[3]) * 1000000

eviction_age = defaultdict(lambda : [])

f = open("results/" + str(tc) + "/out_trace_pop_init_byte.txt" , "r")
reqs = f.readline()
reqs = reqs.strip().split(",")
reqs = [int(r) for r in reqs if r != '']
f.close()
#reqs = reqs[50000000:]
print("Len of trace : ", len(reqs))


f = open("results/" + str(tc) + "/sampled_sizes_pop_init_byte.txt", "r")
sizes = f.readline()
sizes = sizes.strip().split(",")
sizes = [float(s) for s in sizes if s != '']
f.close()

print(len(sizes))

obj_reqs = 0
byte_reqs = 0
obj_hits_fifo = 0
byte_hits_fifo = 0
obj_hits_lru = 0
byte_hits_lru = 0

fifo_c = FIFOCache(cache_size)
lru_c = LRUCache(cache_size)

objects = set()

f = open("results/" + str(tc) + "/generated.stats" +  str(cache_size) + "_all.txt", "w")
#First run the requests for lru and fifo
i = 0
overall_reqs = 0
for r in reqs:

    i += 1
    r = int(r)
    obj_sz = int(sizes[r])

    if i > ignore:
        overall_reqs += 1
        byte_reqs += obj_sz
        obj_reqs += 1

    objects.add(r)

    if i%100000 == 0:
        print("Processed : ", i )
    
    ## Make reqest to fifo
    if fifo_c.get(r) == -1:
        fifo_c.put(r, obj_sz)
    else:
        if i > ignore:
            obj_hits_fifo += 1
            byte_hits_fifo += obj_sz

    ## Make request to LRU
    if lru_c.get(r) == -1:
        lru_c.put(r, obj_sz, eviction_age, i)
    else:
        if i > ignore:
            obj_hits_lru += 1
            byte_hits_lru += obj_sz

    if overall_reqs % 10000 == 0 and i > ignore:# and overall_reqs > 1000000:
        f.write(str(obj_reqs) + " " + str(byte_reqs) + " " + str(obj_hits_fifo) + " " + str(byte_hits_fifo) + " " + str(obj_hits_lru) + " " + str(byte_hits_lru))
        f.write("\n")
        f.flush()
        byte_reqs = 0
        obj_reqs = 0
        obj_hits_fifo = 0
        byte_hits_fifo = 0
        obj_hits_lru = 0
        byte_hits_lru = 0    

f.close()

age_dst = []
## Parse eviction age
for obj in eviction_age:
    times = eviction_age[obj]

    for i in range(int(len(times)/2)):
        enter = times[2*i]
        try:
            leave = times[2*i + 1]
        except:
            break

    age_dst.append(leave - enter)

f = open("results/" + str(tc) + "/age_distribution_generated.txt", "w")
f.write(",".join([str(x) for x in age_dst]))
f.close()
        
        
        
        
