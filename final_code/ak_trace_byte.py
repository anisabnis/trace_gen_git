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

TB = 1000000000
MIL = 1000000

if __name__ == "__main__":
    
    t_len = int(sys.argv[1])
    w_dir = sys.argv[2]

    no_objects = 0
    
    log_file = open("results/" + w_dir + "/log_file.txt", "w")
    log_file.flush()

    popularities = defaultdict()
    sizes = defaultdict()
    iats = defaultdict()

    ## Probability of one hit wonders
    one_hits   = 0
    total_objs = 0

    for i in range(8):
        f = open("results/" + w_dir + "/one_hits_" + str(i) + ".txt")
        l = f.readline()
        l = l.strip().split(" ")
        one_hits += int(l[0])
        total_objs += int(l[1])

    one_hit_pr = float(one_hits)/total_objs

    ## Assign sizes based on popularities
    total_sz = 0
    
    ## Joint distribution of popularity and size
    iat_pop = pop_sz_dst("results/" + w_dir + "/iat_pop_fnl.txt")

    iat_sz = pop_sz_dst("results/" + w_dir + "/iat_sz_fnl.txt")

    ## Joint distribution of iat and stack distance
    fd_sample_opp = pop_sz_dst("results/" + w_dir + "/fd_final.txt", True) 

    ## Sampled iats prior to evaluation

    iat_dst = pop("results/" + w_dir + "/iat_sz_fnl.txt")
    prior_iats = iat_dst.sample_popularities(40*MIL)
    
    req_count = defaultdict(int)    
    i = 0
    j = 0
    while total_sz < 10 * TB:

        if random.random() < one_hit_pr:
            iat = -200
        else:        
            ##Sample an inter-arrival time
            #iat = int(fd_sample_opp.sample(total_sz))        
            iat = prior_iats[j]
            j += 1
            
        iats[i] = iat        
        
        ## Convert inter-arrival time to popularity
        if iat == -200:
            p = 1
            ii = -1
        else:
            p = iat_pop.sample(iat)                
            ii = iat

        ## Use the popularity to sample size
        popularities[i] = p        
        sz = iat_sz.sample(ii)
        total_sz += sz
        sizes[i] = sz
        no_objects += 1        
        req_count[i] = 0
        i += 1

    new_objects = j
        
    print("Len of sizes : ", len(sizes), total_sz)
    
    debug = open("results/" + w_dir + "/debug.txt", "w")

    ## generate random trace
    trace = range(no_objects)
    curr_max_seen = 0
    
    ## create a tree structure using the initial tree
    trace_list, ss = gen_leaves(trace, sizes)
    st_tree, lvl = generate_tree(trace_list)
    root = st_tree[lvl][0]
    root.is_root = True
    curr = st_tree[0][0]

    ## Initialize
    c_trace = []
    tries = 0
    i = 1
    j = 0
    no_desc = 0
    fail = 0
    total_objects = no_objects
    fd_sample = pop_sz_dst("results/" + w_dir + "/fd_final.txt") 
    sampled_fds = []
    sampled_sds_pop = defaultdict(list)
    result_fds = []
    land_pos = []
    land_obj_sz = []

    #f = open("results/" + w_dir + "/prior_sampled_iats.txt", "w")
    #f.write(",".join([str(x) for x in prior_iats]))
    #f.close()

    sz_removed = 0
    sz_added   = 0
    
    while curr != None and i <= t_len:

        pp = popularities[curr.obj_id]            

        if pp > 1:
            
            sd = fd_sample.sample(iats[curr.obj_id])
            sd = int(sd)

            if sd > total_sz:
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
            sz_removed += curr.s
            
        if end_object == False:

            descrepency, land, o_id = root.insertAt(sd, n, 0, curr.id, debug)                            
            
            land_pos.append(land)

            land_obj_sz.append(sizes[o_id])

            local_uniq_bytes = 0

            debug.write("debugline : " + str(local_uniq_bytes) + " " + str(sd) + " " + str(root.s) + " " + str(descrepency) + "\n")

            sampled_fds.append(sd)

            result_fds.append(sd + descrepency)

            if n.parent != None :
                root = n.parent.rebalance(debug)

        else:            

            while True:
                debug.write("debugline : " + str(-1) + " " + str(-1) + " " + str(-1) + " " + str(0) + "\n")

                if random.random() < one_hit_pr:
                    iat = -1
                    p = 1
                else:
                    iat = prior_iats[new_objects]
                    p = iat_pop.sample(iat)
                    
                iats[total_objects] = iat

                popularities[total_objects] = p        

                sz = iat_sz.sample(iat)
                sizes[total_objects] = sz
            
                n = node(total_objects, sz)
                sz_added += sz
            
                req_count[total_objects] = 0
                total_objects += 1
                new_objects += 1
                n.set_b()
                descrepency, x, y = root.insertAt(root.s - 1, n, 0, curr.id, debug)
            
                if n.parent != None:
                    root = n.parent.rebalance(debug)

                if root.s > 10 * TB:
                    break
                    
        next, success = curr.findNext()
        while (next != None and next.b == 0) or success == -1:
            next, success = next.findNext()

        del_nodes = curr.cleanUpAfterInsertion(sd, n, debug)        

        if i % 10001 == 0:
            log_file.write("Trace computed : " +  str(i) + " " +  str(datetime.datetime.now()) +  " " + str(root.s) + " " + str(total_objects) + " " + str(curr_max_seen) + " fail : " + str(fail) + " sz added : " + str(sz_added) + " sz_removed : " + str(sz_removed) + "\n")
            print("Trace computed : " +  str(i) + " " +  str(datetime.datetime.now()) +  " " + str(root.s) + " " + str(total_objects) + " " + str(curr_max_seen) + " fail : " + str(fail) + " sz added : " + str(sz_added) + " sz_removed : " + str(sz_removed))
            log_file.flush()

        curr = next
        i += 1


    log_file.write("Done writing sampled popularities and sizes to file " + str(datetime.datetime.now()) + "\n")
    log_file.flush()

        
    len_c_trace = len(c_trace)
    print("c trace length : ", len_c_trace)

    # if len_c_trace < t_len :
    #     n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
    #     c_trace = c_trace[:n_power_2]
    # else:
    #     n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
    #     c_trace = c_trace[:n_power_2]

    ## Write to disk
    # f = open("results/" + w_dir + "/sampled_popularities.txt", "w")
    # f.write(",".join([str(x) for x in list(popularities.values())]))
    # f.close()

    # f = open("results/" + w_dir + "/sampled_iats.txt", "w")
    # f.write(",".join([str(x) for x in list(iats.values())]))
    # f.close()
    
    # f = open("results/" + w_dir + "/sampled_sizes.txt", "w")
    # f.write(",".join([str(x) for x in list(sizes.values())]))
    # f.close()
        
    # ## Write stats to disk
    f = open("results/" + w_dir + "/sampled_fds_tmp.txt", "w")
    for i in range(len(sampled_fds)):
        f.write(str(sampled_fds[i]) + ",")
    f.close()

    # f = open("results/" + w_dir + "/result_fds.txt", "w")
    # for i in range(len(result_fds)):
    #     f.write(str(result_fds[i]) + ",")
    # f.close()

    # ## b) Number of times each object is in the trace
    # f = open("results/" + w_dir + "/req_count.txt", "w")
    # for i in range(len(req_count)):
    #     f.write(str(req_count[i]) + ",")
    # f.close()

    # ## c) The resulting trace
    # f = open("results/" + w_dir + "/out_trace.txt", "w")
    # for i in range(len(c_trace)):
    #     f.write(str(c_trace[i]) + ",")
    # f.close()    
    # log_file.write("Done writing runtime stats to file " + str(datetime.datetime.now()) + "\n")
    # log_file.flush()

    # ## Land position
    # f = open("results/" + w_dir + "/land_position.txt", "w")
    # for i in range(len(land_pos)):
    #     f.write(str(land_pos[i]) + ",")
    # f.close()

    # plot_list(land_pos)
    # plt.savefig("results/" + w_dir + "/land_position.png")
    # plt.clf()

    # ## Land obj size
    # f = open("results/" + w_dir + "/land_obj_sz.txt", "w")
    # for i in range(len(land_obj_sz)):
    #     f.write(str(land_obj_sz[i]) + ",")
    # f.close()

    # plot_list(land_obj_sz)
    # plt.savefig("results/" + w_dir + "/land_obj_sz.png")
    # plt.clf()



    
