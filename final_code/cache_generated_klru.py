import sys
from lru import *
from util import *
from parser import *
from random_cache import *
import random
import datetime

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
obj_hits = 0
byte_hits = 0

slru_c = KLRUCache(2, cache_size)
objects = set()

if BR == "r":
    f = open("results/" + str(tc) + "/simulations/generated_klru_" +  str(cache_size) + "_" + str(typ) + ".txt", "w")
else:
    f = open("results/" + str(tc) + "/simulations/byte_generated_klru_" +  str(cache_size) + "_" + str(typ) + ".txt", "w")

#First run the requests for lru and fifo
i = 0
overall_reqs = 0
initial_objs = []
initial_tms = {}
initial_sizes = {}
check_objs = {}
initialized = False

eviction_age = []
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

    if i%10000 == 0:
        print("date : ", datetime.datetime.now(), " Processed : ", i )
        #        break

    ## Make reqest to KLRU
    if klru_c.get(r) == -1:
        klru_c.put(r, obj_sz)
    else:
        if i > ignore:
            obj_hits += 1
            byte_hits += obj_sz


    if overall_reqs % 10000 == 0 and i > ignore:# and overall_reqs > 1000000:
        f.write(str(datetime.datetime.now()) + " " + str(obj_reqs) + " " + str(byte_reqs) + " " + str(obj_hits) + " " + str(byte_hits))
        f.write("\n")
        f.flush()
        byte_reqs = 0
        obj_reqs = 0
        obj_hits = 0
        byte_hits = 0

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

# f = open("results/" + str(tc) + "/age_distribution_generated_" + str(css) + ".txt", "w")
# #f.write(",".join([str(x) for x in eviction_age]))
# f.write(str(sum(eviction_age)/len(eviction_age)))
# f.close()
        
        
        
        
