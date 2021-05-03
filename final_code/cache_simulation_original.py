import sys
from lru import *
from fifo import *
from util import *
from parser import *
from random_cache import *
import random

tc = sys.argv[1]
cache_size = int(sys.argv[2]) * 1000000
ignore = 0
mod_u = 120

eviction_age = defaultdict(lambda : [])

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

sizes_real = defaultdict()

if mod_u > 100:
    f = open("results/" + str(tc) + "/simulations/original.stats_"  + str(cache_size) + ".txt", "w")
else:
    f = open("results/" + str(tc) + "/simulations/original.stats_"  + str(cache_size) + "_" + str(mod_u) + ".txt", "w")

if tc == "w":
    input = binaryParser("results/" + str(tc) + "/akamai1.bin")
elif tc == "v":
    input = binaryParser("results/" + str(tc) + "/akamai2.bin")
elif tc == "eu":
    input = euParser("results/" + str(tc) + "/all_sort_int")
elif tc == "tc":
    input = allParser("results/" + str(tc) + "/all.gz")
    
input.open()

overall_reqs = 0
overall_reqs = 0
initial_objs = []
initial_tms = {}
initial_sizes = {}
check_objs = {}
initialized = False

for cnt in range(1):
    i = 0
    j = 1
    objects = set()
    inner_lines = 0

    while True:
        try:
            r, obj_sz, t = input.readline()
        except:
            break

        i += 1
        
        if mod_u < 100 and tc not in [0] :
            continue
        
        obj_sz = int(float(obj_sz)/1000)
        if obj_sz <= 0:
            obj_sz = 1
        
        overall_reqs += 1
        inner_lines += 1

        j += 1
        
        if j % 100000 == 0:
            print("lines read : ", j)

        objects.add(r)
        sizes_real[r] = obj_sz

        #if overall_reqs > 1000000:
        if i > ignore:
            obj_reqs += 1
            byte_reqs += obj_sz

        ## Make reqest to fifo
        if fifo_c.get(r) == -1:
            fifo_c.put(r, obj_sz)
        else:
            #if overall_reqs > 1000000:
            if i > ignore:
                obj_hits_fifo += 1
                byte_hits_fifo += obj_sz

        # ## Make reqest to RANDOM
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
        if lru_c.get(r, eviction_age, i) == -1:
            lru_c.put(r, obj_sz, eviction_age, inner_lines)
        else:
            #if overall_reqs > 1000000:
            if i > ignore:
                obj_hits_lru += 1
                byte_hits_lru += obj_sz

        if overall_reqs % 10000 == 0 and i > ignore:# and overall_reqs > 1000000:
            f.write(str(obj_reqs) + " " + str(byte_reqs) + " " + str(obj_hits_fifo) + " " + str(byte_hits_fifo) + " " + str(obj_hits_lru) + " " + str(byte_hits_lru) + " " + str(obj_hits_rnd) + " " + str(byte_hits_rnd) + "\n")
            f.write("\n")
            f.flush()
            obj_reqs = 0
            byte_reqs = 0
            obj_hits_fifo = 0
            byte_hits_fifo = 0
            obj_hits_lru = 0
            byte_hits_lru = 0            
            obj_hits_rnd = 0
            byte_hits_rnd = 0        

            
        if inner_lines > 200000000:
            break

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

f = open("results/" + str(tc) + "/age_distribution_original.txt", "w")
f.write(",".join([str(x) for x in age_dst]))
f.close()


# print("number of objects : ", len(objects))

# plot_dict(sizes_real, "real")
# plot_list(sizes, "sampled")
# plt.grid()
# plt.legend()
# plt.savefig("results/" + str(tc) + "/size_dst.png")
