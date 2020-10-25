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
    w_dir = sys.argv[3]

    log_file = open("results/" + w_dir + "/log_file.txt", "w")
    log_file.flush()

    sc = 1
    scale_down = 1    

    ## Assign popularities and sizes to each object from the joint distribution
    joint_dst = pop("results/" + w_dir + "/joint_dst.txt")
    popularities = joint_dst.sample_popularities(int(no_objects * 10))
    popularities = np.append(popularities, [1]*8*no_objects)
    plot_list(popularities)
    plt.savefig("results/" + w_dir + "/popdst.png")
    plt.clf()

    sizes = [1] * 100 * no_objects
    log_file.write("Done parsing the size popularity distribution " + str(datetime.datetime.now()) + "\n")
    log_file.flush()


    f = open("results/" + w_dir + "/sampled_popularities.txt", "w")
    f.write(",".join([str(x) for x in popularities]))
    f.close()
    log_file.write("Done writing sampled popularities and sizes to file " + str(datetime.datetime.now()) + "\n")
    log_file.flush()

    ## generate random trace
    trace = range(no_objects)
    curr_max_seen = 0

    ## create a tree structure using the initial tree
    trace_list = gen_leaves(trace, sizes)
    st_tree, lvl = generate_tree(trace_list)
    root = st_tree[lvl][0]
    root.is_root = True
    curr = st_tree[0][0]

    ## Stats to be collected
    req_count = [0] * (15*no_objects)

    ## Initialize
    c_trace = []
    tries = 0
    i = 1
    j = 0
    no_desc = 0
    fail = 0
    total_objects = no_objects
    fd_sample = pop_sz_dst("results/" + w_dir + "/fd_objects.txt", "pop", no_objects) 
    sampled_fds = []
    fd_byte_samples = []
    sampled_sds_pop = defaultdict(list)
    result_fds = []


    joint_dst = pop_sz_dst("results/" + w_dir + "/joint_dst.txt")
    total_sz = 0
    sizes_n = defaultdict(int)
    for i in range(len(popularities)):
        p = popularities[i]
        sizes_n[i] = joint_dst.sample(p)
        if i < no_objects:
            total_sz += sizes_n[i]
        else:
            break

    fd_byte_sample = pop_sz_dst("results/" + w_dir + "/fd_bytes.txt", "pop", total_sz * 1000) 
    ## This is just a debug file
    debug = open("results/" + w_dir + "/debug.txt", "w")

    i = 1
    while curr != None and i <= t_len:

        pp = popularities[curr.obj_id]            

        if pp > 1:
            sd = fd_sample.sample(pp)
            sd_byte = fd_byte_sample.sample(pp)
            sd_byte = int(sd_byte)/1000
            sampled_sds_pop[pp].append(sd)

            if sd_byte > total_sz:
                continue

        else:
            sd = 0

        j += 1
        if sd >= root.s:
            fail += 1
            continue

        n  = node(curr.obj_id, curr.s)        
        n.set_b()
        
        if pp > 0:
            c_trace.append(curr.obj_id)
        else:
            continue

        if curr.obj_id > curr_max_seen:
            curr_max_seen = curr.obj_id

        req_count[curr.obj_id] += 1
        end_object = False

        if req_count[curr.obj_id] >= popularities[curr.obj_id]:
            end_object = True
        
        if end_object == False:

            descrepency, land, o_id = root.insertAt(sd, n, 0, curr.id, debug)                            
            
            local_uniq_bytes = curr.findUniqBytes(n, debug) + 1 * curr.s
            
            debug.write("debugline : " + str(local_uniq_bytes) + " " + str(sd) + " " + str(root.s) + " " + str(descrepency) + "\n")

            sampled_fds.append(sd)

            fd_byte_samples.append(sd_byte)

            result_fds.append(sd + descrepency)

            if n.parent != None :
                root = n.parent.rebalance(debug)

        else:            
            debug.write("debugline : " + str(-1) + " " + str(-1) + " " + str(-1) + " " + str(0) + "\n")

            n = node(total_objects, sizes[total_objects])
            req_count[total_objects] = 0
            total_objects += 1
            n.set_b()
            descrepency, x, y = root.insertAt(root.s - 1, n, 0, curr.id, debug)

            if n.parent != None:
                root = n.parent.rebalance(debug)
               
        next, success = curr.findNext()
        while (next != None and next.b == 0) or success == -1:
            next, success = next.findNext()

        del_nodes = curr.cleanUpAfterInsertion(sd, n, debug)        

        if i % 10001 == 0:
            log_file.write("Trace computed : " +  str(i) + " " +  str(datetime.datetime.now()) +  " " + str(root.s) + " " + str(total_objects) + " " + str(curr_max_seen) + " fail : " + str(fail) + "\n")
            print("Trace computed : " +  str(i) + " " +  str(datetime.datetime.now()) +  " " + str(root.s) + " " + str(total_objects) + " " + str(curr_max_seen) + " fail : " + str(fail))
            log_file.flush()

        curr = next
        i += 1


    len_c_trace = len(c_trace)
    print("c trace length : ", len_c_trace)

    if len_c_trace < t_len :
        n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
        c_trace = c_trace[:n_power_2]
    else:
        n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
        c_trace = c_trace[:n_power_2]

    debug.close()
    
    ## Write stats to disk
    ## a) Sampled stack distances
    f = open("results/" + w_dir + "/sampled_unit_fds.txt", "w")
    for i in range(len(sampled_fds)):
        f.write(str(sampled_fds[i]) + ",")
    f.close()

    f = open("results/" + w_dir + "/sampled_byte_fds.txt", "w")
    for i in range(len(fd_byte_samples)):
        f.write(str(fd_byte_samples[i]) + ",")
    f.close()

    f = open("results/" + w_dir + "/result_unit_fds.txt", "w")
    for i in range(len(result_fds)):
        f.write(str(result_fds[i]) + ",")
    f.close()

    ## b) Number of times each object is in the trace
    f = open("results/" + w_dir + "/req_count.txt", "w")
    for i in range(len(req_count)):
        f.write(str(req_count[i]) + ",")
    f.close()

    ## c) The resulting trace
    f = open("results/" + w_dir + "/out_trace.txt", "w")
    for i in range(len(c_trace)):
        f.write(str(c_trace[i]) + ",")
    f.close()    
    log_file.write("Done writing runtime stats to file " + str(datetime.datetime.now()) + "\n")
    log_file.flush()

    debug = open("results/" + w_dir + "/debug_post.txt", "w")

    fd2, sfd2, sds2, max_sd = gen_sd_dst(c_trace, sizes, sc, t_len, log_file, debug)        
    f = open("results/" + w_dir + "/res_fd.txt", "w")
    for i in range(len(fd2)):
       f.write(str(sds2[i]) + " " + str(fd2[i]) + "\n")
       if i%1000 == 0:
           log_file.write("i : " + str(i))
           log_file.flush()
    f.close()
    plt.plot(sds2, fd2, label="result")
    plot_list(sampled_fds)    
    plt.grid()
    plt.legend()
    plt.savefig("results/" + w_dir + "/stack_distance_unit.png")

    # assign sizes based on popularity and recompute the stack distance curve
    popularities = defaultdict(int)
    for o in c_trace:
        popularities[o] += 1

    all_objects = popularities.keys()
    all_objects.sort()
    sizes = defaultdict(int)

    for o in all_objects:
        p = popularities[o]
        sizes[o] = joint_dst.sample(p)

    f = open("results/" + w_dir + "/assigned_sizes.txt", "w")
    for s in sizes:
        f.write(str(sizes[s]) + ",")
    f.close()

    fd2, sfd2, sds2, max_sd = gen_sd_dst(c_trace, sizes, sc, t_len, log_file, debug)        
    f = open("results/" + w_dir + "/res_fd_byte.txt", "w")
    for i in range(len(fd2)):
       f.write(str(sds2[i]) + " " + str(fd2[i]) + "\n")
       if i%1000 == 0:
           log_file.write("i : " + str(i))
           log_file.flush()
    f.close()

    plt.clf()
    plt.plot(sds2, fd2, label="result", marker="o", markevery=200)
    plot_list(fd_byte_samples, "sample")    
    plt.grid()
    plt.legend()
    plt.savefig("results/" + w_dir + "/stack_distance_byte.png")
    
