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


if __name__ == "__main__":
    
    t_len = int(sys.argv[1])
    no_objects = int(sys.argv[2])
    del_rate = float(sys.argv[3])
    sc = 1
    scale_down = 1

    ## get the footprint descriptor
    print("start : ", datetime.datetime.now())
    fd = FD("./", "sfd.txt", 131072)
    print("parsed footprint descriptor at : ", datetime.datetime.now())

    ## create n objects and set size to 1
    total_objects = no_objects
    sizes = [1 for x in range(20 * no_objects)]
    
    req_count = [0] * (20*no_objects)

    ## Assign popularities to each object
    #
    joint_dst = pop("joint_dst.txt")
    popularities = joint_dst.sample_popularities(no_objects)
    popularities = np.append(popularities, [1] * (20*no_objects))
    #popularities = [float(1)/(p) for p in popularities]

    f = open("sampled_popularities_" + str(del_rate) + ".txt", "w")
    f.write(",".join([str(x) for x in popularities]))
    f.close()

    ## generate random trace
    trace = range(no_objects)
    curr_max_seen = 0

    ## sample fds
    sampled_fds = np.random.choice(fd.sds, 1.4 * t_len, p=fd.sds_pdf)
    sampled_fds = [int(x)/scale_down for x in sampled_fds]

    ## create a tree structure using the initial tree
    trace_list = gen_leaves(trace, sizes)
    st_tree, lvl = generate_tree(trace_list)
    root = st_tree[lvl][0]
    root.is_root = True
    curr = st_tree[0][0]

    print("Root.size : ", root.s)    

    descs = defaultdict(int)
    c_trace = []
    tries = 0
    i = 1
    j = 0
    no_desc = 0
    fail = 0

    while i <= 1.4*t_len:

        try:
            sd = sampled_fds[j]
            j += 1
            if sd >= root.s:
                fail += 1
                continue
        except:
            break

        n = root.removeAt(sd, None, 0, 0)
        root.insertAt(0, n, 0, 0)

        c_trace.append(n.obj_id)
        
        if n.parent != None:
            n.parent.rebalance()

        if n.obj_id > curr_max_seen:
            curr_max_seen = curr.obj_id

        req_count[n.obj_id] += 1

        if i % 50000 == 0:
            print("Trace computed : ", i, datetime.datetime.now(), root.s, curr_max_seen)

        i += 1

    len_c_trace = len(c_trace)
    print("len trace : ", len_c_trace)
        
    if len_c_trace < t_len :
        n_power_2 = np.power(2, np.ceil(math.log(len(c_trace), 2)))
        to_fill = n_power_2 - len_c_trace
        sub_trace = pop.get_trace1(sizes, to_fill)
        c_trace = c_trace + sub_trace
    else:
        n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
        c_trace = c_trace[:n_power_2]


    f = open("out_trace_" + str(del_rate) + ".txt", "w")
    f.write(",".join([str(x) for x in c_trace]))
    f.close()

#     ## plot_the uniq bytes distribution
#     fd2, sfd2, sds2 = gen_sd_dst(c_trace, sizes, sc, t_len)
#     plt.plot(sds2, fd2, label="alg")    
#     plt.plot(fd.sds, fd.sds_pr, label="orig_fd")
#     plt.grid()
#     plt.legend()
#     plt.savefig("sd_uniq_bytes_"+ str(del_rate) + ".png")
#     plt.clf()

    i = 0
    popularity = defaultdict(int)
    for o in c_trace:
        popularity[o] += 1    
        i += 1
        if i % 100000 == 0:
            print("Parsed trace : ", i)

    ## This code writes the popularity of each object onto disk! Just plot it later
    f = open("popularities_trace_" + str(del_rate) + "_.txt" , "w")
    i = 0
    len_ctrace = len(c_trace)
    for o in popularity:
        popularity[o] = float(popularity[o])/len_ctrace
        f.write(str(o) + " " + str(popularity[o]) + "\n")
        i += 1
        if i % 10000 == 0:
            print("assigned popularities : ", i)
    f.close()

    #Assign size to an object based on its popularity
    sz  = obj_size("./", "subtrace.txt.sizeCntObj.json")
    sizes = sz.get_objects(20 * no_objects)
#     joint_dst = pop_sz_dst("joint_dst.txt")
#     objects = list(popularity.keys())
#     objects.sort()
#     sizes = defaultdict(lambda : 1)
#     for o in objects:
#         sizes[o] = joint_dst.sample(popularity[o])

    # Writes the sizes of each object onto disk! Jut plot it later
    f = open("sampled_sizes_" + str(del_rate) + ".txt" ,"w")
    for s in sizes:
        f.write(str(sizes[s]) + ",")
    f.close()


    fd2, sfd2, sds2, max_sd = gen_sd_dst(c_trace, sizes, sc, t_len)
        
    # sd with bytes
    fd = FD("./", "sfd_bytes.txt", max_sd * 1000)    

    
    ## write the resultant stack distance onto file
    f = open("res_fd_" + str(del_rate) + ".txt", "w")
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
