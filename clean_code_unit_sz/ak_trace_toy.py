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

    ## generate random trace
    trace = range(no_objects)
    curr_max_seen = 0
    sizes = [1] * 1000 * no_objects

    ## create a tree structure using the initial tree
    trace_list = gen_leaves(trace, sizes)
    st_tree, lvl = generate_tree(trace_list)
    root = st_tree[lvl][0]
    root.is_root = True
    curr = st_tree[0][0]

    ## Stats to be collected
    descs1 = defaultdict(int)
    descs2 = defaultdict(int)
    land_position1 = defaultdict(list)
    land_position2 = defaultdict(list)
    object_landed_on = []
    req_count = [0] * (1000*no_objects)

    ## Initialize
    c_trace = []
    tries = 0
    i = 1
    j = 0
    no_desc = 0
    fail = 0
    total_objects = no_objects
    sampled_fds = []
    sampled_sds_pop = defaultdict(list)

    #popularities = [1] * 3 * t_len

    ## This is just a debug file
    debug = open("results/" + w_dir + "/debug.txt", "w")

    while curr != None and i <= 1.4 * t_len:

        sd = random.randint(2, no_objects)

        j += 1
        if sd >= root.s:
            fail += 1
            continue

        sampled_fds.append(sd)

        n  = node(curr.obj_id, curr.s)        
        n.set_b()
        c_trace.append(curr.obj_id)

        if curr.obj_id > curr_max_seen:
            curr_max_seen = curr.obj_id

        req_count[curr.obj_id] += 1
        end_object = False

        #if req_count[curr.obj_id] >= popularities[curr.obj_id]:
        if random.random() > 0.8:
            end_object = True
        
        if end_object == False:
            descrepency, land, o_id = root.insertAt(sd, n, 0, curr.id, debug)                


            local_uniq_bytes = curr.findUniqBytes(n, debug) + 1 * curr.s
            
            debug.write("debugline : " + str(local_uniq_bytes) + " " + str(sd) + " " + str(root.s) + " " + str(descrepency) + "\n")

            if n.parent != None :
                root = n.parent.rebalance(debug)
        else:            
            n = node(total_objects, sizes[total_objects])
            req_count[total_objects] = 0
            total_objects += 1
            n.set_b()

            descrepency, x, y = root.insertAt(root.s-1, n, 0, curr.id, debug)
            if n.parent != None:
                root = n.parent.rebalance(debug)
               
        next, success = curr.findNext()
        while (next != None and next.b == 0) or success == -1:
            next, success = next.findNext()

        del_nodes = curr.cleanUpAfterInsertion(sd, n, debug)        

        debug.write("---------------------------------------- \n")

        if i % 50001 == 0:
            log_file.write("Trace computed : " +  str(i) + " " +  str(datetime.datetime.now()) +  " " + str(root.s) + " " + str(total_objects) + " " + str(curr_max_seen) + " fail : " + str(fail) + "\n")
            log_file.flush()

        curr = next
        i += 1

#     len_c_trace = len(c_trace)

#     if len_c_trace < t_len :
#         n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
#         c_trace = c_trace[:n_power_2]
#     else:
#         n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
#         c_trace = c_trace[:n_power_2]


#     debug.close()

#     ## Write stats to disk
#     ## a) Sampled stack distances
#     f = open("results/" + w_dir + "/sampled_fds.txt", "w")
#     for i in range(len(sampled_fds)):
#         f.write(str(sampled_fds[i]) + ",")
#     f.close()

#     ## b) Number of times each object is in the trace
#     f = open("results/" + w_dir + "/req_count.txt", "w")
#     for i in range(len(req_count)):
#         f.write(str(req_count[i]) + ",")
#     f.close()

#     ## c) The resulting trace
#     f = open("results/" + w_dir + "/out_trace.txt", "w")
#     for i in range(len(c_trace)):
#         f.write(str(c_trace[i]) + ",")
#     f.close()

#     ## d) Write the objects on which the sd landed, for each request
#     f = open("results/" + w_dir + "/obj_landed_on.txt", "w")
#     for i in range(len(object_landed_on)):
#         f.write(str(object_landed_on[i]) + ",")
#     f.close()
            
#     ## e) Distribution of descrepency in stack distance experienced
#     with open("results/" + w_dir + "/descrepency1.json", 'w') as outfile:
#         json.dump(descs1, outfile)

#     with open("results/" + w_dir + "/descrepency2.json", 'w') as outfile:
#         json.dump(descs2, outfile)


#     ## f) Distribution of where exactly the object landed (in buckets of 0.001)
#     with open("results/" + w_dir + "/land_position1.json", 'w') as outfile:
#         json.dump(land_position1, outfile)

#     with open("results/" + w_dir + "/land_position2.json", 'w') as outfile:
#         json.dump(land_position2, outfile)
    
#     log_file.write("Done writing runtime stats to file " + str(datetime.datetime.now()) + "\n")
#     log_file.flush()

#     ## g) write the resultant stack distance onto file
#     fd2, sfd2, sds2, max_sd = gen_sd_dst(c_trace, sizes, sc, t_len, log_file)        
#     f = open("results/" + w_dir + "/res_fd.txt", "w")
#     for i in range(len(fd2)):
#         f.write(str(sds2[i]) + " " + str(fd2[i]) + "\n")
#         if i%1000 == 0:
#             log_file.write("i : " + str(i))
#             log_file.flush()
#     f.close()

#     # sd with bytes
#     fd = FD("./results/" + w_dir, "./sfd_bytes.txt", max_sd * 1000)        
#     plt.clf()
#     plt.plot(sds2, fd2, label="alg")    
#     fd_sds = [int(x)/(1000 * scale_down) for x in fd.sds]
#     plt.plot(fd_sds, fd.sds_pr, label="orig_fd")
#     plt.grid()
#     plt.legend()
#     plt.savefig("./results/" + w_dir + "/fd_compare.png")
