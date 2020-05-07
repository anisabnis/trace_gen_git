from treelib import *
from collections import defaultdict
from gen_trace import *
from obj_size_dst import *
from obj_pop_dst import *
from parse_fd import *
from obj_sz_syn_dst import *
from popularity import *
from util_theory import *
from util import *

import matplotlib.pyplot as plt
import random
import datetime
import sys
import math

if __name__ == "__main__":
            
    t_len = int(sys.argv[1])
    no_objects = int(sys.argv[2])
    max_obj_sz = 1000
    sc = 1

    values = range(1, max_obj_sz + 1)
    p = [1 for x in values]
    sum_p = sum(p)
    p = [float(x)/sum_p for x in p]
    sizes = np.random.choice(values, no_objects, p)

    print("Done sampling objects")

    #obj_dst = obj_size_uniform(1, max_obj_sz)
    #sizes, dst = obj_dst.get_objects(no_objects)

    f = open("sampled_sizes.txt", "w")
    for s in sizes:
        f.write(str(s) + ",")
    f.close()

    pop = PopularityDst(0.8)
    pop.assignPopularities(sizes)    

    print("Assigned object popularities")
       
    trace = pop.get_trace1(sizes, t_len)

    fd, sfd1, sds1 = gen_sd_dst(trace, sizes, sc, t_len)

    trace = pop.get_trace(sizes, t_len)


    trace_list = gen_leaves(trace, sizes)
    st_tree, lvl = generate_tree(trace_list)
    root = st_tree[lvl][0]
    curr = st_tree[0][0]

    print(root.s)

    sampled_fds = np.random.choice(sds1, 3*t_len, p=sfd1)

    print("Done sampling fds", max(sampled_fds))

    plot_list(sampled_fds)

    f = open("sampled_sds.txt", "w")
    for s in sampled_fds:
        f.write(str(s) + ",")
    f.close()

    descs = defaultdict(int)
    c_trace = []
    tries = 0
    i = 0
    j = 0
    no_desc = 0

    f2 = open("success.txt", "w")
    
    while curr != None and i < 2*t_len:
        try:
            sd = sampled_fds[j]
            j += 1
        except:
            break

#         if sd >= root.s:
#             i += 1
#             tries += 1

#             if tries > 10:
#                 nn = curr.next
#                 if nn != None:
#                     nn.set_b()
#                     nn.update_till_root()

#                 next, success = curr.findNext()
#                 while (next != None and next.b == 0) or success == -1:
#                     next, success = next.findNext()
                    
#                 c_trace.append(curr.obj_id)
#                 curr.delete_node()
#                 curr = next
#                 tries = 0

#             continue

        n  = node(curr.obj_id, curr.s)        
        n.set_b()
        c_trace.append(curr.obj_id)
        
        descrepency = root.insertAt(sd, n, 0, curr.id)                
        descs[descrepency] += 1

        ## If the object is going to be inserted right next to it then 
        ## do not insert it there. Come up with a cleaner solution later!
        if descrepency == "Na" :
            no_desc += 1
            continue
    
        next, success = curr.findNext()
        while (next != None and next.b == 0) or success == -1:
            next, success = next.findNext()
        
        del_nodes = curr.cleanUpAfterInsertion(sd, n)        
        n.update_till_root()

        if i % 1000 == 0:
            print("Trace computed : ", i, datetime.datetime.now(), root.s)

        f2.write(str(sd) + ",")
        
        curr = next
        i += 1
            
    print("Number of descrepencies : ", no_desc)

    #plot_dict(descs)
    #plt.savefig("descs.png")
    #plt.clf()
    
    len_c_trace = len(c_trace)

    print("Length of trace : ", len_c_trace)

    if len_c_trace < t_len :
        n_power_2 = np.power(2, np.ceil(math.log(len(c_trace), 2)))
        to_fill = n_power_2 - len_c_trace
        sub_trace = pop.get_trace1(sizes, to_fill)
        c_trace = c_trace + sub_trace
        print("1 : ", len(c_trace))
    else:
        n_power_2 = int(np.power(2, np.floor(math.log(len(c_trace), 2))))
        print("2 : ", n_power_2)
        c_trace = c_trace[:n_power_2]

    print("Length of c trace finally : ", len(c_trace))

    fd2, sfd2, sds2 = gen_sd_dst(c_trace, sizes, sc, t_len)#len_c_trace)

    plt.plot(sds1, fd, label="orig")
    plt.plot(sds2, fd2, label="alg")
    plt.grid()
    plt.legend()
    plt.savefig("fd_compare.png")

    f = open("out_trace.txt", "w")
    for i,o in enumerate(c_trace):
        try :
            if c_trace[i+1] == c_trace[i]:
                continue
        except:
            pass

        f.write(str(o))
        f.write(",")        
    f.close()
