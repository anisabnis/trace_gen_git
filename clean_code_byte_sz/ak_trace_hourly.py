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
#import matplotlib.pyplot as plt
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
    popularities = joint_dst.sample_popularities(int(no_objects) * 3)
    #popularities.sort(reverse=True)
    #popularities = np.append(popularities, [1]*8*no_objects)
    #plot_list(popularities)
    #plt.savefig("results/" + w_dir + "/popdst.png")
    #plt.clf()

    ## Assign sizes based on popularities
    total_sz = 0
    joint_dst = pop_sz_dst("results/" + w_dir + "/joint_dst.txt")
    sizes = []
    for i in range(len(popularities)):
        p = popularities[i]
        sz = joint_dst.sample(p)
        sizes.append(sz)
        if i < no_objects:
            total_sz += sizes[i]
        else:
            continue

    print("Len of sizes : ", len(sizes), total_sz)


    debug = open("results/" + w_dir + "/debug.txt", "w")

    ## Write to disk
    f = open("results/" + w_dir + "/sampled_popularities.txt", "w")
    f.write(",".join([str(x) for x in popularities]))
    f.close()

    f = open("results/" + w_dir + "/sampled_sizes.txt", "w")
    f.write(",".join([str(x) for x in sizes]))
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

    ## collect request hours
    req_hr = []
    f = open("results/" + w_dir + "/req_hr.txt", "r")
    for l in f:
        l = int(l.strip())
        req_hr.append(l)
    r_hr = 0
    curr_tm = 0

    ## Initialize
    c_trace = []
    tries = 0
    i = 1
    j = 0
    no_desc = 0
    fail = 0
    total_objects = no_objects
    fd_samples = []
    for i in range(len(req_hr)):        
        fd_sample = pop_sz_dst("results/" + w_dir + "/fd_bytes_" + str(i) + ".txt", "pop", total_sz * 1000) 
        fd_samples.append(fd_sample)
        if i >= 47:
            break
        
    sampled_fds = []
    sampled_sds_pop = defaultdict(list)
    result_fds = []
    land_pos = []
    land_obj_sz = []

    sampled_fds_hourly = defaultdict(list)

    i = 1

    while curr != None and i <= t_len:

        pp = popularities[curr.obj_id]            

        if pp > 1:
            sd = fd_samples[curr_tm].sample(pp - 1)
            sd = int(sd/1000)
            sampled_fds_hourly[curr_tm].append(sd)
            if sd > total_sz:
                continue
        else:
            sd = 0

        r_hr += 1
        if r_hr > req_hr[curr_tm]:
            curr_tm += 1
            r_hr = 0

        if curr_tm >= 47:
            print("curr_time : ", curr_tm)
            break

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
            
            land_pos.append(land)

            land_obj_sz.append(sizes[o_id])

            #local_uniq_bytes = curr.findUniqBytes(n, debug) + 1 * curr.s
            local_uniq_bytes = 0

            debug.write("debugline : " + str(local_uniq_bytes) + " " + str(sd) + " " + str(root.s) + " " + str(descrepency) + "\n")

            sampled_fds.append(sd)

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
    
    ## Write stats to disk
    f = open("results/" + w_dir + "/sampled_fds.txt", "w")
    for i in range(len(sampled_fds)):
        f.write(str(sampled_fds[i]) + ",")
    f.close()

    f = open("results/" + w_dir + "/result_fds.txt", "w")
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

    ## d) write samples for each hour
    for t in sampled_fds_hourly:
        ss = sampled_fds_hourly[t]
        f = open("results/" + w_dir + "/sampled_fds_" + str(t) + ".txt", "w")
        f.write(",".join([str(x) for x in ss]))
        f.close()

    ## Land position
    f = open("results/" + w_dir + "/land_position.txt", "w")
    for i in range(len(land_pos)):
        f.write(str(land_pos[i]) + ",")
    f.close()

    #plot_list(land_pos)
    #plt.savefig("results/" + w_dir + "/land_position.png")
    #plt.clf()

    ## Land obj size
    f = open("results/" + w_dir + "/land_obj_sz.txt", "w")
    for i in range(len(land_obj_sz)):
        f.write(str(land_obj_sz[i]) + ",")
    f.close()

    #plot_list(land_obj_sz)
    #plt.savefig("results/" + w_dir + "/land_obj_sz.png")
    #plt.clf()

    asdf

    fd2, sfd2, sds2, max_sd = gen_sd_dst(c_trace, sizes, sc, t_len, log_file, debug)        
    f = open("results/" + w_dir + "/res_fd.txt", "w")
    for i in range(len(fd2)):
       f.write(str(sds2[i]) + " " + str(fd2[i]) + "\n")
       if i%1000 == 0:
           log_file.write("i : " + str(i))
           log_file.flush()
    f.close()
    #plt.clf()
    #plt.plot(sds2, fd2, label="result") #, marker="o", markersize=3, markevery=400)
    #plot_list(sampled_fds)    
    #plt.grid()
    #plt.legend()
    #plt.savefig("results/" + w_dir + "/stack_distance_byte.png")


    
