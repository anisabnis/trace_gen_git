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
    
    log_file = open("results/" + w_dir + "/log_file.txt", "w")
    log_file.flush()

    f = open("results/" + w_dir + "/footprint_desc_all.txt", "r")
    l = f.readline().strip().split(" ")
    one_hit_pr = float(l[-1])/float(l[0])
    f.close()

    iat_dst = pop("results/" + w_dir + "/iat_sz_all.txt", 0 , TB)
    iats = iat_dst.sample_popularities(50*MIL)
    iat_sz_dst = pop_sz_dst("results/" + w_dir + "/iat_sz_all.txt", 0, TB)
    sizes = []
    for iat in iats:
        sz = iat_sz_dst.sample(iat)
        sizes.append(sz)

    # sz_dst = pop_opp("results/" + w_dir + "/iat_sz_all.txt", 0 , TB)
    # sizes = sz_dst.sample_keys(50*MIL)

    # ## Assign iats to the objects
    # iat_sz_dst = pop_sz_dst("results/" + w_dir + "/iat_sz_all.txt", True, TB , 0)
    # iats = []
    # for s in sizes:
    #     iat = iat_sz_dst.sample(s)
    #     iats.append(iat)


    total_sz   = 0
    total_objects = 0
    i = 0
    while total_sz < 10*TB:
        total_sz += sizes[total_objects]
        total_objects += 1
        if total_objects % 100000 == 0:
            print(total_objects, total_sz)
        
        
    print("total objects : ", total_objects)
        
    debug = open("results/" + w_dir + "/debug.txt", "w")

    ## generate random trace
    trace = range(total_objects)
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
    i = 0
    j = 0
    k = 0
    no_desc = 0
    fail = 0

    #fd_sample = pop_opp2("results/" + w_dir + "/", 0, 1000*TB)
    #stack_samples = fd_sample.sample_keys(MIL)
    fd_sample = pop_sz_dst("results/" + w_dir + "/footprint_desc_all.txt")
    
    sampled_fds = []
    sampled_sds_pop = defaultdict(list)
    result_fds = []
    land_pos = []
    land_obj_sz = []

    sz_added   = 0
    sz_removed = 0
    evicted_ = 0
    
    while curr != None and i <= t_len:

        sd = fd_sample.sample(iats[curr.obj_id])
        
        if sd >= root.s:
            fail += 1
            continue
            
        end_object = False
        ## Introduce a new object
        if random.random() < one_hit_pr:
            end_object = True
            sz_removed += curr.s
            evicted_ += 1
        else:
            sd = random.randint(sd, sd+200000)         
            
        n  = node(curr.obj_id, curr.s)        
        n.set_b()

        c_trace.append(n.obj_id)

        if curr.obj_id > curr_max_seen:
            curr_max_seen = curr.obj_id            
            
        if end_object == False:

            try:
                descrepency, land, o_id = root.insertAt(sd, n, 0, curr.id, debug)                            
            except:
                print("sd : ", sd, root.s)
                
            land_pos.append(land)

            land_obj_sz.append(sizes[o_id])

            local_uniq_bytes = 0

            debug.write("debugline : " + str(local_uniq_bytes) + " " + str(sd) + " " + str(root.s) + " " + str(descrepency) + "\n")

            sampled_fds.append(sd)

            result_fds.append(sd + descrepency)

            if n.parent != None :
                root = n.parent.rebalance(debug)

        else:
            while root.s < 10*TB:
                
                if (total_objects + 1) % (50*MIL) == 0:
                    iats_n = iat_dst.sample_keys(50*MIL)
                    iats.extend(iats_n)

                    for iat in iats_n:
                        sz = iat_sz_dst.sample(iat)
                        sizes.append(sz)
                    
                total_objects += 1
                sz = sizes[total_objects]
                sz_added += sz
                n = node(total_objects, sz)
                n.set_b()        
                descrepency, x, y = root.insertAt(root.s - 1, n, 0, curr.id, debug)
            
                if n.parent != None:
                    root = n.parent.rebalance(debug)
                                    
        next, success = curr.findNext()
        while (next != None and next.b == 0) or success == -1:
            next, success = next.findNext()

        del_nodes = curr.cleanUpAfterInsertion(sd, n, debug)        

        if i % 10001 == 0:
            log_file.write("Trace computed : " +  str(i) + " " +  str(datetime.datetime.now()) +  " " + str(root.s) + " " + str(total_objects) + " " + str(curr_max_seen) + " fail : " + str(fail) + " sz added : " + str(sz_added) + " sz_removed : " + str(sz_removed) + "\n")
            print("Trace computed : " +  str(i) + " " +  str(datetime.datetime.now()) +  " " + str(root.s) + " " + str(total_objects) + " " + str(curr_max_seen) + " fail : " + str(fail) + " sz added : " + str(sz_added) + " sz_removed : " + str(sz_removed) + " evicted : " +  str(evicted_))
            log_file.flush()

        curr = next
        i += 1

        
    ## Write sampled sizes to disk    
    f = open("results/" + w_dir + "/sampled_sizes_iat.txt", "w")
    f.write(",".join([str(x) for x in sizes]))
    f.close()
        
    # ## Write stats to disk
    f = open("results/" + w_dir + "/sampled_fds_iat.txt", "w")
    for i in range(len(sampled_fds)):
        f.write(str(sampled_fds[i]) + ",")
    f.close()

    # ## Write the trace to dist
    f = open("results/" + w_dir + "/out_trace_iat.txt", "w")
    for i in range(len(c_trace)):
        f.write(str(c_trace[i]) + ",")
    f.close()    



    
