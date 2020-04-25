import sys
from collections import defaultdict
import copy
import numpy as np
import matplotlib.pyplot as plt

def gen_fd(trace):
    fd_d = defaultdict(lambda : 0)
    counter = 0
    sc = 1000

    for i in range(len(trace)):        
        if i%1000 == 0:
            print("generating fd : ", i)

        uniq_bytes = 0
        curr_item = trace[i][1]
        uniq_objects = set()
        success = False

        for k in range(i + 1, len(trace)):
            if trace[k][1] == curr_item:
                #uniq_bytes += sizes[curr_item]
                success = True
                break
            else:
                if trace[k][1] not in uniq_objects:
                    uniq_bytes += trace[k][2]
                    uniq_objects.add(trace[k][1])
             

        if success == True:
            key =  int(float(uniq_bytes)/sc) * sc
            fd_d[key] += 1
        else:
            counter += 1


    ks = list(fd_d.keys())
    ks.sort()

    counts = []
    for k in ks:
        counts.append(fd_d[k])

    #ks = [sc * k for k in ks]
        
    sum_counts = sum(counts)
    counts = [float(x)/sum_counts for x in counts]
    
    s_counts = copy.deepcopy(counts)
    
    counts = np.cumsum(counts)
    
    #plt.plot(ks, counts, label=label)
   # plt.savefig("fd.png")

    print("counter : ", counter)
    return counts, s_counts, ks
    

f = open("data_30/sub_trace.txt", "r")
trace = []
sz_dst = defaultdict(int)
pop_dst = defaultdict(int)
for l in f:
    l = l.strip().split(" ")
    l = [int(x) for x in l]
    sz = l[2]
    oid = l[1]
    sz_dst[sz] += 1
    pop_dst[oid] += 1
    trace.append(l)

fd, sfd1, sds1 = gen_fd(trace)

plt.plot(sds1, fd, label="original")
plt.savefig("Fd.png")
plt.clf()

sizes = list(sz_dst.keys())
sizes.sort()
vals = []
for s in sizes:
    vals.append(sz_dst[s])
sum_vals = sum(vals)
vals = [float(x)/sum_vals for x in vals]
vals = np.cumsum(vals)
plt.plot(sizes, vals)
plt.savefig("size_dst.png")
plt.clf()

oids = list(pop_dst.keys())
oids.sort()
vals = []
for o in oids:
    vals.append(pop_dst[o])
sum_vals = sum(vals)
vals = [float(x)/sum_vals for x in vals]
vals = np.cumsum(vals)
plt.plot(range(len(oids)), vals)
plt.savefig("pop_dst.png")
plt.clf()
