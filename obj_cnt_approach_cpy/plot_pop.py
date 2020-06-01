import sys
import numpy as np
import matplotlib.pyplot as plt
from joint_dst import *


k = sys.argv[1]

# with open("./subtrace.txt.popCntReq.json", "r") as read_file:
#     pop_dst = json.load(read_file)

# print("total objects : ", len(pop_dst))
# pops = list(pop_dst.keys())
# pops = [int(x.encode("utf-8")) for x in pops]
# pops.sort()
# pop_prs = []
# for s in pops:
#     s = unicode(str(s), "utf-8")
#     pop_prs.append(pop_dst[s])
# sum_pr = sum(pop_prs)
# pop_prs = [float(p)/sum_pr for p in pop_prs]
# pop_prs.sort(reverse=True)
# pop_prs = np.cumsum(pop_prs)
# plt.plot(pop_prs)
# plt.xlabel("Objects")
# plt.ylabel("CDF")
# plt.grid()
# plt.savefig("pop1_" + k + ".png")
# plt.clf()


f = open("joint_dst.txt", "r")
key = int(f.readline())
no_objects = 0
freq_list = []
for l in f:
    l = l.strip().split(" ")
    if len(l) == 1:
        freq_list.extend([key]*no_objects)
        key = int(l[0])
        no_objects = 0
    else:
        no_objects += int(l[1])

freq_list.sort(reverse=True)
n = int(len(freq_list)/4)
freq_list = freq_list[:n]
sum_f = sum(freq_list)
freq_list = [float(x)/sum_f for x in freq_list]
freq_list = np.cumsum(freq_list)
plt.plot(freq_list, label="orig")

#plt.xlabel("Objects")
#plt.ylabel("CDF")
#plt.grid()
#plt.savefig("pop_joint.png")

small_len = len(freq_list)
f = open("popularities_trace_" + k + "_.txt", "r")
popularities = []
for l in f:
    l = l.strip().split(" ")
    p = float(l[1])
    popularities.append(p)

popularities.sort(reverse=True)
popularities = popularities[:n]
sum_p = sum(popularities)
popularities = [float(p)/sum_p for p in popularities]
popularities = np.cumsum(popularities)
big_len = len(popularities)
keys = range(len(popularities))
#keys = [float(i)*(float(small_len)/big_len) for i in keys]
#keys = keys[:n]
#popularities = popularities[:n]
plt.grid()
plt.plot(keys, popularities, label="alg")
plt.xlabel("Objects")
plt.ylabel("CDF")
plt.legend()
plt.savefig("pop_" + k + ".png")



    
