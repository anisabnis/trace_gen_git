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
    tc = sys.argv[3]

    ## colon seperated
    all_tcs = sys.argv[4]

    ## colon seperated
    ratios = sys.argv[5]
    
    MAX_SD = 0
    ## get maximum stack distance
    f = open("results/" + w_dir + "/calculus_footprint_desc_" + str(tc) +".txt", "r")
    for l in f:
        l = l.strip().split(" ")
        sd = int(float(l[1]))
        if sd > MAX_SD:
            MAX_SD = sd
    f.close()

    if w_dir == "tc":
        MAX_SD = min(1.5*TB, MAX_SD)
    elif w_dir == "sm":
        MAX_SD = min(2.8*TB, MAX_SD)
    else:
        MAX_SD = 10*TB
                
    log_file = open("results/" + w_dir + "/log_file_" + str(tc) + ".txt", "w")
    log_file.flush()
    
    sz_dsts = []
    tcs = all_tcs.split(":")
    ratios = ratios.split(":")
    ratios = [int(x) for x in ratios]
    fnl_ratios = []
    sz_ratios = []
    def find_uniqrate(f):
        urate = 0
        l = f.readline()
        for l in f:
            l = l.strip().split(" ")
            iat = int(l[0])
            sd  = int(l[1])
            rt = float(sd)/(iat + 100)
            pr = float(l[2])
            urate += pr * rt
        return urate    

    for i in range(len(tcs)):
        f = open("results/" + w_dir + "/footprint_desc_" + tcs[i] + ".txt", "r")        
        uniq_bytes = 10000 * find_uniqrate(f)        
        sz_dst = pop_opp("results/" + w_dir + "/iat_sz_" + str(tcs[i]) + ".txt", 0 , TB)
        sz_dsts.append(sz_dst)
        total_sz = 0
        no_objects = 0
        while total_sz < uniq_bytes:
            total_sz += sz_dst.sample_keys(1)[0]
            no_objects += 1
        fnl_ratios.append(ratios[i]*no_objects)
    sum_ratios = sum(fnl_ratios)
    fnl_ratios = [float(x)/sum_ratios for x in fnl_ratios]
        
    total_sz = 0 
    n_sizes = []
    sizes = []
    for i in range(len(tcs)-1):
        n_sizes.extend(sz_dsts[i].sample_keys(int(fnl_ratios[i]*70*MIL)))    
    n_sizes.extend(sz_dsts[i+1].sample_keys(int(70*MIL - len(n_sizes))))
    random.shuffle(n_sizes)
    sizes.extend(n_sizes)                   

    print("done sampling sizes ", len(sizes))
    
    total_sz   = 0
    total_objects = 0
    i = 0
    while total_sz < MAX_SD:
        total_sz += sizes[total_objects]
        total_objects += 1
        if total_objects % 100000 == 0:
            print(total_objects, total_sz)

    print("total objects : ", total_objects)
    
    debug = open("results/" + w_dir + "/debug_" + str(tc) + ".txt", "w")

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

    fd_sample = object_sd("results/" + w_dir + "/calculus_footprint_desc_" + str(tc) +".txt", 0, 1000*TB)
    stack_samples = fd_sample.sample_keys([], [], 1000)
    land_obj_sz = []

    sz_added   = 0
    sz_removed = 0
    evicted_ = 0

    sizes_seen = []
    sds_seen   = []

    sampled_fds = []
    
    while curr != None and i <= t_len:

        if k >= 1000:
            stack_samples = fd_sample.sample_keys(sizes_seen, sds_seen, 1000)
            sizes_seen = []
            sds_seen = []
            k = 0

        sd = stack_samples[k]
        sds_seen.append(sd)
        sizes_seen.append(curr.s)
        
        k += 1                    
        end_object = False
        ## Introduce a new object
        if sd < 0 or sd >= root.s:
            end_object = True
            sz_removed += curr.s
            evicted_ += 1
            sd = -1
        else:
            sd = random.randint(sd, sd+200000)         

            
        n  = node(curr.obj_id, curr.s)        
        n.set_b()

        c_trace.append(n.obj_id)

        if curr.obj_id > curr_max_seen:
            curr_max_seen = curr.obj_id
            
        sampled_fds.append(sd)
            
        if end_object == False:

            try:
                descrepency, land, o_id = root.insertAt(sd, n, 0, curr.id, debug)                            
            except:
                print("sd : ", sd, root.s)
                
            local_uniq_bytes = 0

            debug.write("debugline : " + str(local_uniq_bytes) + " " + str(sd) + " " + str(root.s) + " " + str(descrepency) + "\n")

            if n.parent != None :
                root = n.parent.rebalance(debug)

        else:
            while root.s < MAX_SD:

                if (total_objects + 1) % (70*MIL) == 0:
                    
                    n_sizes = []
                    for ij in range(len(tcs)-1):
                        n_sizes.extend(sz_dsts[ij].sample_keys(int(fnl_ratios[i]*70*MIL)))
                    n_sizes.extend(sz_dsts[ij+1].sample_keys(int(70*MIL - len(n_sizes))))
                    random.shuffle(n_sizes)
                    sizes.extend(n_sizes)                    
                
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
    f = open("results/" + w_dir + "/sampled_sizes_" +str(tc) + ".txt", "w")
    f.write(",".join([str(x) for x in sizes]))
    f.close()
        
    # ## Write stats to disk
    f = open("results/" + w_dir + "/sampled_fds_" + str(tc) + ".txt", "w")
    for i in range(len(sampled_fds)):
        f.write(str(sampled_fds[i]) + ",")
    f.close()

    # ## Write the trace to dist
    f = open("results/" + w_dir + "/out_trace_" + str(tc) + ".txt", "w")
    for i in range(len(c_trace)):
        f.write(str(c_trace[i]) + ",")
    f.close()    



    
