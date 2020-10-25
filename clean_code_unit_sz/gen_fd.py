import sys

from treelib import *
from gen_trace import *
from util import *
import numpy as np
import math

f_name = sys.argv[1]
f = open(f_name, "r")
l = f.readline()
l = l.strip().split(",")
c_trace = l[:-1]
c_trace = [int(x) for x in c_trace]
f.close()

n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
c_trace = c_trace[:n_power_2]

o_name = sys.argv[2]
f = open(f_name, "r")
l = f.readline()
l = l.strip().split(",")
sizes = l[:-1]
sizes = [int(x) for x in sizes]
f.close()

sc = 1
scale_down = 1
t_len = 33554432

fd2, sfd2, sds2, max_sd = gen_sd_dst(c_trace, sizes, sc, t_len)
        
# sd with bytes
fd = FD("./", "sfd_bytes.txt", max_sd * 1000)    
    
## write the resultant stack distance onto file
f = open("res_fd.txt", "w")
for i in range(len(fd2)):
    f.write(str(sds2[i]) + " " + str(fd2[i]) + "\n")
f.close()
    
plt.clf()
plt.plot(sds2, fd2, label="alg")    
fd_sds = [int(x)/(1000 * scale_down) for x in fd.sds]
plt.plot(fd_sds, fd.sds_pr, label="orig_fd")
plt.grid()
plt.legend()
plt.savefig("fd_compare_" + str(del_rate) + ".png")

