import sys
from lru import *
from fifo import *
from util import *
import random

tc = sys.argv[1]
cache_size = int(sys.argv[2]) * 1000000

# f = open("results/" + str(tc) + "/out_trace.txt" , "r")
# reqs = f.readline()
# reqs = reqs.strip().split(",")
# reqs = [int(r) for r in reqs if r != '']
# f.close()

reqs_6hr = []
f = open("results/" + tc + "/req_hr.txt", "r")
ttl_reqs = 0
for l in f:
    l = int(l.strip())
    ttl_reqs += l
    reqs_6hr.append(l)
    if ttl_reqs > 33554432:
        break
ttl_tm = len(reqs_6hr)
f.close()

print(reqs_6hr)

print("len of trace : ", len(reqs))

# f = open("results/" + str(tc) + "/sampled_sizes.txt", "r")
# sizes = f.readline()
# sizes = sizes.strip().split(",")
# sizes = [int(s) for s in sizes if s != '']
# f.close()

obj_reqs = 0
byte_reqs = 0
obj_hits_fifo = 0
byte_hits_fifo = 0
obj_hits_lru = 0
byte_hits_lru = 0

fifo_c = FIFOCache(cache_size)
lru_c = LRUCache(cache_size)

objects = set()

# f = open("results/" + str(tc) + "/generated.stats" +  str(cache_size) + ".txt", "w")
# #First run the requests for lru and fifo
# i = 0
# overall_reqs = 0

# curr_tm = 0
# count_reqs = 0
# for r in reqs:

#     i += 1
#     r = int(r)
#     obj_sz = int(sizes[r])

#     overall_reqs += 1

#     #if overall_reqs > 1000000:

#     if overall_reqs < 25000000:
#         continue

#     byte_reqs += obj_sz
#     obj_reqs += 1

#     objects.add(r)

#     count_reqs += 1

#     ## Make reqest to fifo
#     if fifo_c.get(r) == -1:
#         fifo_c.put(r, obj_sz)
#     else:
#         #if overall_reqs > 1000000:
#         obj_hits_fifo += 1
#         byte_hits_fifo += obj_sz

#     ## Make request to LRU
#     if lru_c.get(r) == -1:
#         lru_c.put(r, obj_sz)
#     else:
#         #if overall_reqs > 1000000:
#         obj_hits_lru += 1
#         byte_hits_lru += obj_sz

#     if count_reqs >= reqs_6hr[curr_tm%(ttl_tm-1)]:# and overall_reqs > 1000000:
#         f.write(str(obj_reqs) + " " + str(byte_reqs) + " " + str(obj_hits_fifo) + " " + str(byte_hits_fifo) + " " + str(obj_hits_lru) + " " + str(byte_hits_lru))
#         f.write("\n")
#         f.flush()
#         print("requests completed : ", obj_reqs)
#         byte_reqs = 0
#         obj_reqs = 0
#         obj_hits_fifo = 0
#         byte_hits_fifo = 0
#         obj_hits_lru = 0
#         byte_hits_lru = 0
#         curr_tm += 1
#         count_reqs = 0

    #if i > 80000000:
    #    break


total_objects = len(objects)
f.close()

print(len(objects))
#asdf
total_reqs = obj_reqs

obj_reqs = 0
byte_reqs = 0
obj_hits_fifo = 0
byte_hits_fifo = 0
obj_hits_lru = 0
byte_hits_lru = 0

fifo_c = FIFOCache(cache_size)
lru_c = LRUCache(cache_size)

sizes_real = defaultdict()

#all_objects = set()
## Next run the trace in the original.
#f1 = open("trace_" + str(tc) + ".txt", "r")
#for l in f1:
#    obj = l.strip().split(" ")[1]
#    all_objects.add(obj)
#f1.close()

#all_objects = list(all_objects)
#print("len(all_objects)", len(all_objects))

#sample_objects = random.choices(all_objects, k=total_objects)
#req_objects = defaultdict(int)
#for o in sample_objects:
#    req_objects[o] = 1

f = open("results/" + str(tc) + "/original.stat"  + str(cache_size) + ".txt", "w")
curr_tm = 0
overall_reqs = 0
count_reqs = 0
for cnt in range(1):
    f1 = open("trace_" + str(tc) + ".txt", "r")
    i = 0
    j = 0
    objects = set()
    inner_lines = 0

    for l in f1:
        
        overall_reqs += 1
        inner_lines += 1

        j += 1
    
        if j % 10000 == 0:
            print("lines read : ", j)

        l = l.strip().split(" ")
        t = l[2]

        r = l[1]

        r = int(l[1])
        objects.add(r)
        obj_sz = int(int(l[3])/1000)
        sizes_real[r] = obj_sz

        #if overall_reqs > 1000000:
        obj_reqs += 1
        byte_reqs += obj_sz

        i += 1
        count_reqs += 1

        ## Make reqest to fifo
        if fifo_c.get(r) == -1:
            fifo_c.put(r, obj_sz)
        else:
            #if overall_reqs > 1000000:
            obj_hits_fifo += 1
            byte_hits_fifo += obj_sz

        ## Make request to LRU
        if lru_c.get(r) == -1:
            lru_c.put(r, obj_sz)
        else:
            #if overall_reqs > 1000000:
            obj_hits_lru += 1
            byte_hits_lru += obj_sz

        if count_reqs >= reqs_6hr[curr_tm%(ttl_tm-1)]:# and overall_reqs > 1000000:
            f.write(str(obj_reqs) + " " + str(byte_reqs) + " " + str(obj_hits_fifo) + " " + str(byte_hits_fifo) + " " + str(obj_hits_lru) + " " + str(byte_hits_lru))
            f.write("\n")
            f.flush()
            print("requests completed : ", obj_reqs)    
            obj_reqs = 0
            byte_reqs = 0
            obj_hits_fifo = 0
            byte_hits_fifo = 0
            obj_hits_lru = 0
            byte_hits_lru = 0
            curr_tm += 1
            count_reqs = 0

        if inner_lines > 33554432:
            break

    f1.close()

f.close()

print("number of objects : ", len(objects))

plot_dict(sizes_real, "real")
plot_list(sizes, "sampled")
plt.grid()
plt.legend()
plt.savefig("results/" + str(tc) + "/size_dst.png")
