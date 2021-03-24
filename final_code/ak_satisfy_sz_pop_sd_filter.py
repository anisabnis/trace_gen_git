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
        
    ## Assign popularities and sizes to each object from the joint distribution
    total_objects = 0
    no_objects = 0
    popularities = []
    req_count = []
    sizes = []
    f = open("results/" + w_dir + "/cache_state_0_8.txt", "r")    
    total_sz = 0
    for l in f:
        l = l.strip().split(",")
        sz = float(l[2])
        p  = int(l[1])
        popularities.append(p)
        sizes.append(sz)
        req_count.append(int(l[3]))
        total_objects += 1
        no_objects += 1
        total_sz += sz


    i = len(sizes)
    ## First sample sizes
    sz_dst = pop_opp("results/" + w_dir + "/joint_dst_0_sz.txt", 0, TB)
    obj_left = 50*MIL - len(sizes)
    sizes.extend(sz_dst.sample_keys(obj_left))
        
    ## Assign sizes based on popularities
    sz_pop = pop_sz_dst("results/" + w_dir + "/joint_dst_0_sz.txt", True)
    while total_sz < 10 * TB:
        sz = sizes[i]
        p = sz_pop.sample(sz)
        popularities.append(p)
        total_sz += sizes[i]
        total_objects += 1
        no_objects    += 1
        i += 1

        if total_objects % 100000 == 0:
            print("Total objects : ", total_objects)
            
    while no_objects < 50*MIL:
        sz = sizes[i]
        p  = sz_pop.sample(sz)
        popularities.append(p)        
        no_objects += 1
        i += 1
            
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

    fd_sample = joint_dst("results/" + w_dir + "/sz_sd_0.txt", False, 0)

    fd_sample_2 = pop_opp3("results/" + w_dir + "/sz_sd_0.txt", 1, TB)
    sizes_req = fd_sample_2.p_keys
    sizes_pr  = fd_sample_2.pr
    accept_pr = defaultdict(lambda : 1)
    
    sampled_fds = []
    sampled_sds_pop = defaultdict(list)
    result_fds = []
    land_pos = []
    land_obj_sz = []

    sz_added   = 0
    sz_removed = 0
    evicted_ = 0

    req_count.extend([0] * (25*total_objects))


    def recompute_accept_pr(sizes_seen):
        req_count = defaultdict(lambda : 0)
        total = 0
        for sz in sizes_seen:
            req_count[sz] += 1
            total += 1
        acc_pr = defaultdict(lambda : 1)
        for i, sz in enumerate(sizes_req):
            if sz in req_count:
                p = float(req_count[sz])/total
                acc_pr[sz] = sizes_pr[i]/p
            else:
                acc_pr[sz] = 1
        return acc_pr
            

    sizes_seen = []
    while curr != None and i <= t_len:

        ## Sample based on size of the object
        sz = sizes[curr.obj_id]        
        sizes_seen.append(sz)
        
        if sz > 0:
            sd = fd_sample.sample(sz)
            if sd > total_sz:
                continue
        else:
            sd = 0
        
        if sd >= root.s:
            fail += 1
            continue
                        
        n  = node(curr.obj_id, curr.s)        
        n.set_b()

        c_trace.append(n.obj_id)

        if curr.obj_id > curr_max_seen:
            curr_max_seen = curr.obj_id
            
        req_count[curr.obj_id] += 1            

        ## Introduce a new object, ending the current object
        #if req_count[curr.obj_id] >= popularities[curr.obj_id]:
        if np.random.random() > accept_pr[sz]:
            sz_removed += curr.s
            evicted_ += 1

            sampled_fds.append(10*TB + 200000)
            
            while root.s < 10*TB:

                if (total_objects + 1) % (50*MIL) == 0:
                    sizes_n = sz_dst.sample_keys(50*MIL)
                    sizes.extend(sizes_n)

                    for sz in sizes_n:
                        p = sz_pop.sample(sz)
                        popularities.append(p)
                                
                total_objects += 1
                sz = sizes[total_objects]
                sz_added += sz
                n = node(total_objects, sz)
                n.set_b()                
                descrepency, x, y = root.insertAt(root.s - 1, n, 0, curr.id, debug)
            
                if n.parent != None:
                    root = n.parent.rebalance(debug)
            
        else:
            sd = random.randint(sd, sd+200000)         

            sampled_fds.append(sd)            

            try:
                descrepency, land, o_id = root.insertAt(sd, n, 0, curr.id, debug)                            
            except:
                print("sd : ", sd, root.s)
                
            land_pos.append(land)

            land_obj_sz.append(sizes[o_id])

            local_uniq_bytes = 0

            debug.write("debugline : " + str(local_uniq_bytes) + " " + str(sd) + " " + str(root.s) + " " + str(descrepency) + "\n")

            result_fds.append(sd + descrepency)

            if n.parent != None :
                root = n.parent.rebalance(debug)

                                    
        next, success = curr.findNext()
        while (next != None and next.b == 0) or success == -1:
            next, success = next.findNext()

        del_nodes = curr.cleanUpAfterInsertion(sd, n, debug)        

        if i % 10001 == 0:
            log_file.write("Trace computed : " +  str(i) + " " +  str(datetime.datetime.now()) +  " " + str(root.s) + " " + str(total_objects) + " " + str(curr_max_seen) + " fail : " + str(fail) + " sz added : " + str(sz_added) + " sz_removed : " + str(sz_removed) + "\n")
            print("Trace computed : " +  str(i) + " " +  str(datetime.datetime.now()) +  " " + str(root.s) + " " + str(total_objects) + " " + str(curr_max_seen) + " fail : " + str(fail) + " sz added : " + str(sz_added) + " sz_removed : " + str(sz_removed) + " evicted : " +  str(evicted_))
            log_file.flush()


        if i % 100000 == 0:
            accept_pr = recompute_accept_pr(sizes_seen)
            sizes_seen = []
            

            
        curr = next
        i += 1

        
    ## Write sampled sizes to disk    
    f = open("results/" + w_dir + "/sampled_sizes_sz_pop_init.txt", "w")
    f.write(",".join([str(x) for x in sizes]))
    f.close()

    ## Write sampled popularities to disk
    f = open("results/" + w_dir + "/sampled_pop_sz_pop_init.txt", "w")
    f.write(",".join([str(x) for x in popularities]))
    f.close()
    
    # ## Write stats to disk
    f = open("results/" + w_dir + "/sampled_fds_sz_pop_init.txt", "w")
    for i in range(len(sampled_fds)):
        f.write(str(sampled_fds[i]) + ",")
    f.close()

    # ## Write the trace to dist
    f = open("results/" + w_dir + "/out_trace_sz_pop_init.txt", "w")
    for i in range(len(c_trace)):
        f.write(str(c_trace[i]) + ",")
    f.close()    

    ## See if each object is represent sufficient number of times
    ## in the trace
    f = open("results/" + w_dir + "/req_count_sz_pop_init.txt", "w")
    for i in range(len(req_count)):
        f.write(str(req_count[i]) + ",")
    f.close()    



    
