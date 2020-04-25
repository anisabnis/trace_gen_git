import sys
from collections import defaultdict
import numpy as np
import copy

dir="/mnt/nfs/scratch1/asabnis/data/binary/" + sys.argv[1]
    
def gen_fd2(trace):
    fd_d = defaultdict(lambda : 0)
    counter = 0
    sc = 200

    for i in range(len(trace)):
        if i%1000 == 0:
            print("generating fd : ", i)

        uniq_bytes = 0
        curr_item = trace[i][0]
        uniq_objects = set()
        success = False

        for k in range(i + 1, len(trace)):
            if trace[k][0] == curr_item:
                success = True
                break
            else:
                if trace[k][0] not in uniq_objects:
                    uniq_bytes += trace[k][1]
                    uniq_objects.add(trace[k][0])

        if success == True:
            key = int(float(uniq_bytes)/sc) * sc
            fd_d[key] += 1
        else:
            counter += 1


    ks = list(fd_d.keys())
    ks.sort()

    counts = []
    for k in ks:
        counts.append(fd_d[k])

    sum_counts = sum(counts)
    counts = [float(x)/sum_counts for x in counts]

    s_counts = copy.deepcopy(counts)

    counts = np.cumsum(counts)
    return counts, s_counts, ks

trace_f = open(dir + "/subtrace.txt", "r")
trace = []
i = 0
for l in trace_f:
    i += 1
    l = l.strip().split(" ")
    oid = int(l[1])
    sz  = int(l[2])
    trace.append([oid, sz])

trace_f.close()

fd_file = open(dir + "/FD.txt", "w")
fd, sfd, sds = gen_fd2(trace)
for i in range(len(fd)):
    fd_file.write(str(sds[i]) + " " + str(sfd[i]) + " " + str(fd[i]) + "\n")
fd_file.close()
