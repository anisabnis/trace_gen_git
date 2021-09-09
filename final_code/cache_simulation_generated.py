import sys
from lru import *
from fifo import *
from util import *
from parser import *
from random_cache import *
import random

tc = sys.argv[1]
css = int(sys.argv[2])
cache_size =  css * 1000000
#ignore = int(sys.argv[3]) * 1000000
ignore = 0
typ = sys.argv[3]
BR = sys.argv[4]

eviction_age = []

if BR == "r":
    f = open("results/" + str(tc) + "/out_trace_" + typ +".txt" , "r")
else:
    f = open("results/" + str(tc) + "/byte_out_trace_" + typ +".txt" , "r")
    
reqs = f.readline()
reqs = reqs.strip().split(",")
reqs = [int(r) for r in reqs if r != '']
min_len = min(len(reqs), 10000000)
reqs = reqs[:min_len]
f.close()
print("Len of trace : ", len(reqs))

if BR == "r":
    f = open("results/" + str(tc) + "/sampled_sizes_" + typ + ".txt", "r")
else:
    f = open("results/" + str(tc) + "/byte_sampled_sizes_" + typ + ".txt", "r")
    
sizes = f.readline()
sizes = sizes.strip().split(",")
sizes = [float(s) for s in sizes if s != '']
f.close()


obj_reqs = 0
byte_reqs = 0
obj_hits_fifo = 0
byte_hits_fifo = 0
obj_hits_lru = 0
byte_hits_lru = 0
obj_hits_rnd = 0
byte_hits_rnd = 0

fifo_c = FIFOCache(cache_size)
lru_c = LRUCache(cache_size)
rnd_c = RNDCache(cache_size)
objects = set()

if BR == "r":
    f = open("results/" + str(tc) + "/simulations/generated_stats_" +  str(cache_size) + "_" + str(typ) + ".txt", "w")
else:
    f = open("results/" + str(tc) + "/simulations/byte_generated_stats_" +  str(cache_size) + "_" + str(typ) + ".txt", "w")

#First run the requests for lru and fifo
i = 0
overall_reqs = 0
initial_objs = []
initial_tms = {}
initial_sizes = {}
check_objs = {}
initialized = False


total_bytes_req = 0

for r in reqs:

    i += 1
    r = int(r)
    obj_sz = int(sizes[r])

    total_bytes_req += obj_sz
    
    if i > ignore:
        overall_reqs += 1
        byte_reqs += obj_sz
        obj_reqs += 1

    objects.add(r)

    if i%100000 == 0:
        print("Processed : ", i )
        #        break

    ## Make reqest to fifo
    if fifo_c.get(r) == -1:
        fifo_c.put(r, obj_sz)
    else:
        if i > ignore:
            obj_hits_fifo += 1
            byte_hits_fifo += obj_sz

    ## Make reqest to RANDOM
    # if i < 50000:
    #     if r not in check_objs:
    #         check_objs[r] = 1
    #         initial_objs.append(r)
    #         initial_sizes[r] = obj_sz
    #         initial_tms[r] = 0
    # elif initialized == False:
    #     rnd_c.initialize(initial_objs, initial_sizes, initial_tms)
    #     initialized = True
    # else:
    #     sd, tm = rnd_c.insert(r, obj_sz, 0)
    #     if sd != -1:
    #         if i > ignore:
    #             obj_hits_rnd += 1
    #             byte_hits_rnd += obj_sz


    ## Make request to LRU
    if lru_c.get(r, total_bytes_req)[0] == -1:
        lru_c.put(r, (obj_sz, total_bytes_req), eviction_age)
    else:
        if i > ignore:
            obj_hits_lru += 1
            byte_hits_lru += obj_sz

    if overall_reqs % 10000 == 0 and i > ignore:# and overall_reqs > 1000000:
        f.write(str(obj_reqs) + " " + str(byte_reqs) + " " + str(obj_hits_fifo) + " " + str(byte_hits_fifo) + " " + str(obj_hits_lru) + " " + str(byte_hits_lru) + " " + str(obj_hits_rnd) + " " + str(byte_hits_rnd))
        f.write("\n")
        f.flush()
        byte_reqs = 0
        obj_reqs = 0
        obj_hits_fifo = 0
        byte_hits_fifo = 0
        obj_hits_lru = 0
        byte_hits_lru = 0    
        obj_hits_rnd = 0
        byte_hits_rnd = 0        

    if i > 80000000:
        break

        
f.close()

# age_dst = []
# ## Parse eviction age
# for obj in eviction_age:
#     times = eviction_age[obj]

#     for i in range(int(len(times)/2)):
#         enter = times[2*i]
#         try:
#             leave = times[2*i + 1]
#         except:
#             break

#     age_dst.append(leave - enter)

f = open("results/" + str(tc) + "/age_distribution_generated_" + str(css) + ".txt", "w")
#f.write(",".join([str(x) for x in eviction_age]))
f.write(str(sum(eviction_age)/len(eviction_age)))
f.close()
        
        
        
        
