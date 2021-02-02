from treelib import *
from gen_trace import *
from parse_fd import *
from util import *
from collections import defaultdict
import matplotlib.pyplot as plt
import sys
import math
import numpy as np

tc = sys.argv[1]

req_hr = []
f = open( "results/" + str(tc) + "/req_hr.txt", "r")
for l in f:
    l = int(l.strip())
    req_hr.append(l)

reqs = []
sizes = defaultdict()
#f = open("trace_" + str(tc) + ".txt", "r")
f = open("all_sort_int", "r")
i = 0

objects = defaultdict(int)
oid = 0

for l in f:
    l = l.strip().split(" ")
    r = str(l[1]) + ":" + str(l[2])
    if r not in objects:
        objects[r] = oid
        co = oid
        oid += 1
    else :
        co = objects[r]

    reqs.append(co)
    sz = int(int(l[3]))
    sizes[co] = sz
    i += 1

    if i > 69108864:
        break

    #if i > 524288:
    #    break

    if i > 1048576:
        break

f.close()

n_power_2 = int(np.power(2, np.floor(math.log(len(reqs), 2))))
reqs = reqs[:n_power_2]

log_file = open("results/" + str(tc) + "/log_file_2.txt", "w")
debug = open("results/" + str(tc) + "/debug.txt", "w")

fd, popularity = gen_sd_dst_oid(reqs, sizes, 1000, len(reqs), req_hr)
for t in fd:
    f = open("results/" + str(tc) + "/original_" + str(t) + ".txt", "w")
    save_list(fd[t],f)
    f.close()

