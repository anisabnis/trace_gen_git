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

reqs = []
sizes = defaultdict()
f = open("trace_" + str(tc) + ".txt", "r")
i = 0

for l in f:
    l = l.strip().split(" ")
    r = int(l[1])
    reqs.append(r)
    sz = int(int(l[3]))
    sizes[r] = sz
    i += 1

    if i > 33554452:
        break

f.close()

n_power_2 = int(np.power(2, np.floor(math.log(len(reqs), 2))))
reqs = reqs[:n_power_2]


log_file = open("results/" + str(tc) + "/log_file_2.txt", "w")
debug = open("results/" + str(tc) + "/debug.txt", "w")

fd2, sfd2, sds2, max_sd = gen_sd_dst(reqs, sizes, 1000, len(reqs), log_file, debug)        
f = open("results/" + str(tc) + "/original_trace_fd.txt", "w") 
for i in range(len(fd2)):
    f.write(str(sds2[i]) + " " + str(fd2[i]) + "\n")
f.close()
