import sys
from lru import *
from fifo import *
from util import *
from parser import *
from random_cache import *
from climb import *
import random

tc = sys.argv[1]
css = int(sys.argv[2])
cache_size =  css * 1000000
ignore = 0
mod_u = 120

eviction_age = []

obj_reqs = 0
byte_reqs = 0
obj_hits = 0
byte_hits = 0

climb_c = CLIMBCache(cache_size)

sizes_real = defaultdict()

if mod_u > 100:
    f = open("results/" + str(tc) + "/simulations/original_climb_"  + str(cache_size) + ".txt", "w")
else:
    f = open("results/" + str(tc) + "/simulations/original_climb_"  + str(cache_size) + "_" + str(mod_u) + ".txt", "w")

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

total_bytes_req = 0

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
        total_bytes_req += obj_sz

        
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
        if i < 50:
            if r not in check_objs:
                check_objs[r] = 1
                initial_objs.append(r)
                initial_sizes[r] = obj_sz
                initial_tms[r] = 0
        elif initialized == False:
            climb_c.initialize(initial_objs, initial_sizes, initial_tms)
            initialized = True
        else:
            sd, tm = climb_c.insert(r, obj_sz, 0)
            if sd != -1:
                if i > ignore:
                    obj_hits += 1
                    byte_hits += obj_sz


        if overall_reqs % 10000 == 0 and i > ignore:# and overall_reqs > 1000000:
            f.write(str(obj_reqs) + " " + str(byte_reqs) + " " + str(obj_hits) + " " + str(byte_hits))
            f.write("\n")
            f.flush()
            obj_reqs = 0
            byte_reqs = 0
            obj_hits = 0
            byte_hits = 0
            
        if inner_lines > 80000000:
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

# f = open("results/" + str(tc) + "/age_distribution_original_" + str(css) +  ".txt", "w")
# f.write(str(sum(eviction_age)/(1000*len(eviction_age))))
# #f.write(",".join([str(x) for x in eviction_age]))
# f.close()


# print("number of objects : ", len(objects))

# plot_dict(sizes_real, "real")
# plot_list(sizes, "sampled")
# plt.grid()
# plt.legend()
# plt.savefig("results/" + str(tc) + "/size_dst.png")
