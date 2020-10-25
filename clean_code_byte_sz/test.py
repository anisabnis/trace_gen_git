from treelib import *
from gen_trace import *
from parse_fd import *
from util import *
from collections import defaultdict
import matplotlib.pyplot as plt
import sys

tc = sys.argv[1]

f = open("results/" + str(tc) + "/out_trace.txt" , "r")
reqs = f.readline()
reqs = reqs.strip().split(",")
reqs = [int(r) for r in reqs if r != '']
reqs = reqs[:67108864]
f.close()

f = open("results/" + str(tc) + "/sampled_sizes.txt", "r")
sizes = f.readline()
sizes = sizes.strip().split(",")
sizes = [int(s) for s in sizes if s != '']
f.close()

log_file = open("results/" + str(tc) + "/log_file_2.txt", "w")
debug = open("results/" + str(tc) + "/debug_2.txt", "w")

fd1, sfd1, sds1, max_sd = gen_sd_dst(reqs, sizes, 1, len(reqs), log_file, debug)        
f = open("results/" + str(tc) + "/result_trace_fd_66_mil.txt", "w") 
for i in range(len(fd1)):
    f.write(str(sds1[i]) + " " + str(fd1[i]) + "\n")
f.close()
