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
    fd = FD("./", "sfd.txt", no_objects)
    print("parsed footprint descriptor at : ", datetime.datetime.now())

    ## create n objects and set size to 1
    total_objects = no_objects
    
    req_count = [0] * (7*no_objects)

    ## Assign popularities and sizes to each object from the joint distribution
    joint_dst = pop("joint_dst.txt")
    popularities = joint_dst.sample_popularities(no_objects * 2)
    popularities = np.append(popularities, [1] * (5*no_objects))    

    joint_dst = pop_sz_dst("joint_dst.txt")
    sizes = []
    for i in range(len(popularities)):
        p = popularities[i]
        sizes.append(joint_dst.sample(p))

    f = open("sampled_popularities_" + str(del_rate) + ".txt", "w")
    f.write(",".join([str(x) for x in popularities]))
    f.close()

    f = open("sampled_sizes_" + str(del_rate) + ".txt", "w")
    f.write(",".join([str(x) for x in sizes]))
    f.close()

    ## generate random trace
    trace = range(no_objects)
    curr_max_seen = 0

    ## create a tree structure using the initial tree
    trace_list = gen_leaves(trace, sizes)
    st_tree, lvl = generate_tree(trace_list)
    root = st_tree[lvl][0]
    root.is_root = True
    curr = st_tree[0][0]

    print("root.s : ", root.s)

    descs = defaultdict(int)
    c_trace = []
    tries = 0
    i = 1
    j = 0
    no_desc = 0
    fail = 0

    fd_sample = pop_sz_dst("fd_popularity_bytes.txt", "pop") 
    sampled_fds = []
    sampled_sds_pop = defaultdict(list)

    while curr != None and i <= 1.4 * t_len:

        pp = popularities[curr.obj_id]            
        if pp > 1:
            sd = fd_sample.sample(pp)
            sd = int(float(sd)/1000)
            sampled_fds.append(sd)
            sampled_sds_pop[pp].append(sd)
        else:
            sd = 0

        j += 1
        if sd >= root.s:
            fail += 1
            continue

        n  = node(curr.obj_id, curr.s)        
        n.set_b()
        c_trace.append(curr.obj_id)

        if curr.obj_id > curr_max_seen:
            curr_max_seen = curr.obj_id

        req_count[curr.obj_id] += 1
        end_object = False

        if req_count[curr.obj_id] >= popularities[curr.obj_id]:
            end_object = True
        
        if end_object == False:
            descrepency = root.insertAt(sd, n, 0, curr.id)                
            if n.parent != None :
                n.parent.rebalance()
        else:            
            n = node(total_objects, sizes[total_objects])
            req_count[total_objects] = 0
            total_objects += 1
            n.set_b()
            descrepency = root.insertAt(root.s - 1, n, 0, curr.id)
            if n.parent != None:
                n.parent.rebalance()
               
        next, success = curr.findNext()
        while (next != None and next.b == 0) or success == -1:
            next, success = next.findNext()

        del_nodes = curr.cleanUpAfterInsertion(sd, n)        

        if i % 50001 == 0:
            print("Trace computed : ", i, datetime.datetime.now(), root.s, total_objects, curr_max_seen, "fail : ", fail)

        curr = next
        i += 1

    len_c_trace = len(c_trace)
    print("len_c_trace : ", len_c_trace)

    if len_c_trace < t_len :
        n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
        print("n_pow: ", n_power_2)
        c_trace = c_trace[:n_power_2]
    else:
        n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
        c_trace = c_trace[:n_power_2]


    f = open("sampled_fds_" + str(del_rate) + ".txt", "w")
    f.write(",".join([str(x) for x in sampled_fds]))
    f.close()

    f = open("req_count_" + str(del_rate) + ".txt", "w")
    f.write(",".join([str(x) for x in req_count]))
    f.close()

    f = open("out_trace_" + str(del_rate) + ".txt", "w")
    f.write(",".join([str(x) for x in c_trace]))
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
