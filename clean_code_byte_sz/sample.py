import sys
from treelib import *
from collections import defaultdict
from gen_trace import *
from obj_size_dst import *
from obj_pop_dst import *
from parse_fd import *
import datetime
from util import *
from joint_dst import *
import matplotlib.pyplot as plt
import random
import datetime
import sys
import math

sampleee = defaultdict(list)

w_dir = sys.argv[1]

samples = []

no_objects = 3000000

joint_dst = pop("results/" + w_dir + "/joint_dst.txt")
popularities = joint_dst.sample_popularities(int(no_objects))
# popularities.sort()

# popularities = [x for x in popularities if x > 1]


# plot_list(popularities, label="sample", maxlim=50)
# #print(popularities[:100000])

# ppp = defaultdict(int)
# f = open("trace_" + str(w_dir) + ".txt", "r")
# i = 0
# for l in f:
#     oid = int(l.strip().split(" ")[1])
#     ppp[oid] += 1
#     i += 1
#     if i > 4097152:
#         break

# #ppp = list(ppp.values()).sort()[:2000]
# ppp = list(ppp.values())
# ppp.sort()
# ppp = [x for x in ppp if x > 1]

# #print(ppp[:100000])
# plot_list(ppp, label="orig", maxlim=50)
# plt.grid()
# plt.legend()
# plt.savefig("results/" + str(w_dir) + "/popularity.png")

#asdf

total_sz = 0
joint_dst = pop_sz_dst("results/" + w_dir + "/joint_dst.txt")
for i in range(len(popularities)):
    p = popularities[i]
    sz = joint_dst.sample(p)

    if i < no_objects:
        total_sz += sz
    else:
        continue

total_sz = 800000000000

#total_sz = 100000
fd_sample = pop_sz_dst("results/" + w_dir + "/fd_bytes.txt", "pop", total_sz * 1000) 
i = 1
req_cnt = 0
for p in popularities:
    if p > 1:
        for k in range(p-1):
            sd = fd_sample.sample(p - 1)
            sd = int(sd)/1000
            #if sd <= total_sz:
            samples.append(sd)
            req_cnt += 1
            sampleee[p].append(sd)

    if i % 10000 == 0:
        print("objects processed : ", i)
    i += 1

# f = open("results/4/fd_bytes.txt")
# fds = defaultdict(list)
# prs = defaultdict(list)
# for l in f:
#     l = l.strip().split(" ")
#     if len(l) == 1:
#         key = int(l[0])
#         continue
#     else:
#         fds[key].append(int(l[0])/1000)
#         prs[key].append(float(l[1]))

# for key in sampleee:
#     if key in fds:
#         pr = np.cumsum(prs[key])
#         plt.clf()
#         print(pr)
#         plt.plot(fds[key], pr, label="orig")
#         plot_list(sampleee[key], label="samples")
#         plt.legend()
#         plt.savefig("results/" + str(w_dir) + "/junk/samplee_" + str(key) + ".png")    

# print("req_cnt : ", req_cnt)

plt.clf()

f = open("results/" + str(w_dir) + "/original_trace_fd.txt", "r")
fds = []
prs = []
for l in f:
    l = l.strip().split(" ")
    fd = int(l[0])/1000
    pr = float(l[1])
    fds.append(fd)
    prs.append(pr)

    #if fd > total_sz:
    #    break

#sum_prs = prs[-1]
#prs = [float(pr)/sum_prs for pr in prs]
plt.clf()
plot_list(samples)
plt.plot(fds, prs, label="original")
plt.grid()
plt.legend()
plt.savefig("results/" +  str(w_dir) + "/sample.png")
    



