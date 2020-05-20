import sys
from treelib import *
from collections import defaultdict
from gen_trace import *
from obj_size_dst import *
from obj_pop_dst import *
from parse_fd import *
import datetime
from util import *
import matplotlib.pyplot as plt
import random
import datetime
import sys
import math


if __name__ == "__main__":
    
    t_len = int(sys.argv[1])
    no_objects = int(sys.argv[2])
    sc = 1

    ## get the footprint descriptor
    print("start : ", datetime.datetime.now())
    fd = FD("./", "sfd.txt")
    print("parsed footprint descriptor at : ", datetime.datetime.now())

    ## create n objects and set size to 1
    total_objects = no_objects
    sizes = [1 for x in range(no_objects)]

    ## generate random trace
    trace = range(no_objects)

    sampled_fds = np.random.choice(fd.sds, t_len + 1000, p=fd.sds_pdf)
    ## comment out the line below later
    #sampled_fds = [int(x)/10 for x in sampled_fds]
    print("max sampled sds : ", max(sampled_fds[:t_len/2]), max(fd.sds), len(sampled_fds))

    trace_list = gen_leaves(trace, sizes)
    st_tree, lvl = generate_tree(trace_list)
    root = st_tree[lvl][0]
    root.is_root = True
    curr = st_tree[0][0]

    print("Root.size : ", root.s)    

    descs = defaultdict(int)
    c_trace = []
    tries = 0
    i = 0
    j = 0
    no_desc = 0
    fail = 0

    while curr != None and i <= t_len + 100:

        try:
            sd = sampled_fds[j]
            j += 1
            if sd >= root.s:
                fail += 1
                continue
        except:
            break

        n  = node(curr.obj_id, curr.s)        
        n.set_b()
        c_trace.append(curr.obj_id)

        end_object = False
        if np.random.random() < 0.02:
            end_object = True
        
        if end_object == False:
            descrepency = root.insertAt(sd, n, 0, curr.id)                

            if n.parent != None :
                n.parent.rebalance()
        else:            
            n = node(total_objects, 1)
            n.set_b()
            descrepency = root.insertAt(root.s - 1, n, 0, curr.id)
            if n.parent != None:
                n.parent.rebalance()
    
        next, success = curr.findNext()
        while (next != None and next.b == 0) or success == -1:
            next, success = next.findNext()

        del_nodes = curr.cleanUpAfterInsertion(sd, n)        

        if i % 10000 == 0:
            print("Trace computed : ", i, datetime.datetime.now(), root.s)
        
        curr = next
        i += 1

    len_c_trace = len(c_trace)

    if len_c_trace < t_len :
        n_power_2 = np.power(2, np.ceil(math.log(len(c_trace), 2)))
        to_fill = n_power_2 - len_c_trace
        sub_trace = pop.get_trace1(sizes, to_fill)
        c_trace = c_trace + sub_trace
    else:
        n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
        c_trace = c_trace[:n_power_2]

#     popularity = defaultdict(int)
#     for o in c_trace:
#         popularity[o] += 1

#     for o in popularity:
#         popularity[o] = float(popularity[o])/len(c_trace)


#     joint_dst = pop_sz_dst("./joint_dst.txt")
#     objects = list(popularity.keys())
#     objects.sort()
#     sizes = defaultdict(lambda : 1)
#     for o in objects:
#         sizes[o] = joint_dst.sample(popularity[o])

    fd2, sfd2, sds2 = gen_sd_dst(c_trace, sizes, sc, t_len)

    plot_list(sampled_fds)
    plt.plot(sds2, fd2, label="alg")
    plt.grid()
    plt.legend()
    plt.savefig("fd_compare.png")
