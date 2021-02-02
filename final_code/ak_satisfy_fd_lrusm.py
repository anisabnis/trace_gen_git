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

    fd_sample = pop_opp2("results/" + w_dir + "/footprint_desc_all.txt", 0, 1000*TB)

    sz_dst = pop_opp("results/" + w_dir + "/iat_sz_all.txt", 0 , TB)
    sizes = sz_dst.sample_keys(50*MIL)

    print("done sampling sizes ")
        
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

    stack_samples = fd_sample.sample_keys(MIL)

    sampled_fds = []
    sampled_sds_pop = defaultdict(list)
    result_fds = []
    land_pos = []
    land_obj_sz = []

    sz_added   = 0
    sz_removed = 0
    evicted_ = 0
    

    while i <= t_len:
        
        if k >= MIL:
            stack_samples = fd_sample.sample_keys(MIL)
            k = 0
        
        
        insert_new_object  = False
        ## Introduce a new object
        if random.random() < one_hit_pr:
            insert_new_object = True
            sz_removed += curr.s
            evicted_ += 1
        else:
            sd = stack_samples[k]
            k += 1
            #sd = random.randint(sd, sd+200000)         
            
            if sd >= root.s:
                fail += 1
                continue


        ## If insert new object = True
        if insert_new_object == True:
            if (total_objects + 1) % (50*MIL) == 0:
                sizes_n = sz_dst.sample_keys(50*MIL)
                sizes.extend(sizes_n)

            total_objects += 1
            sz = sizes[total_objects]
            sz_added += sz

            c_trace.append(total_objects)
            
            n = node(total_objects, sz)
            n.set_b()
            
            ## insert object at the top of the cache
            p_c = curr.parent
            root = p_c.add_child_first_pos(n, debug)
            curr = n

            ## Maintain the cache to be of 10TB
            while root.s > 10*TB:

                try:
                    sz, obj = root.delete_last_node(debug)
                    sz_removed += sz
                    
                except:
                    print("failed")
                    asdf
                                    
        else:

            ## find the object at the distance
            n = root.deleteAt(sd, debug)
            c_trace.append(n.obj_id)

            ## insert at the top of the cache
            p_c = curr.parent
            root = p_c.add_child_first_pos(n, debug)
            curr = n

            sampled_fds.append(sd)
            
        

        if i % 10001 == 0:
            log_file.write("Trace computed : " +  str(i) + " " +  str(datetime.datetime.now()) +  " " + str(root.s) + " " + str(total_objects) + " fail : " + str(fail) + " sz added : " + str(sz_added) + " sz_removed : " + str(sz_removed) + "\n")
            print("Trace computed : " +  str(i) + " " +  str(datetime.datetime.now()) +  " " + str(root.s) + " " + str(total_objects) + " fail : " + str(fail) + " sz added : " + str(sz_added) + " sz_removed : " + str(sz_removed) + " evicted : " +  str(evicted_))
            log_file.flush()

        i += 1
        

                
    ## Write sampled sizes to disk    
    f = open("results/" + w_dir + "/sampled_sizes_lrusm.txt", "w")
    f.write(",".join([str(x) for x in sizes]))
    f.close()
        
    # ## Write stats to disk
    f = open("results/" + w_dir + "/sampled_fds_lrusm.txt", "w")
    for i in range(len(sampled_fds)):
        f.write(str(sampled_fds[i]) + ",")
    f.close()

    # ## Write the trace to dist
    f = open("results/" + w_dir + "/out_trace_lrusm.txt", "w")
    for i in range(len(c_trace)):
        f.write(str(c_trace[i]) + ",")
    f.close()    
