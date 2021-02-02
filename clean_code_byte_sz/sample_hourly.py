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

no_objects = 30000000

joint_dst = pop("results/" + w_dir + "/joint_dst.txt")
popularities = joint_dst.sample_popularities(int(no_objects))


req_hr = []
f = open("results/" + w_dir + "/req_hr.txt", "r")
for l in f:
    l = int(l.strip())
    req_hr.append(l)
r_hr = 0
curr_tm = 0

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
fd_samples = []
for i in range(len(req_hr)):        
    fd_sample = pop_sz_dst("results/" + w_dir + "/fd_bytes_" + str(i) + ".txt", "pop", total_sz * 1000) 
    fd_samples.append(fd_sample)

i = 1
req_cnt = 0
for p in popularities:
    if p > 1:
        for k in range(p-1):
            sd = fd_samples[curr_tm].sample(p - 1)
            sd = int(sd)/1000
            #if sd <= total_sz:
            samples.append(sd)
            req_cnt += 1
            sampleee[p].append(sd)
            r_hr += 1
            if r_hr > req_hr[curr_tm]:
                curr_tm += 1
                r_hr = 0



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
plot_list(samples, label="sampled")
plt.plot(fds, prs, label="original")
plt.grid()
plt.legend()
plt.savefig("results/" +  str(w_dir) + "/sample.png")
    



