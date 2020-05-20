import sys
from treelib import *
from collections import defaultdict
from gen_trace import *
from obj_size_dst import *
from obj_pop_dst import *
from parse_fd import *
import datetime
from util import *
from util_theory import *
import matplotlib.pyplot as plt
import random
import datetime
import sys
import math


if __name__ == "__main__":
    
    t_len = int(sys.argv[1])
    no_objects = int(sys.argv[2])
    del_rate = float(sys.argv[3])
    sc = 1
    sc_fd = 1000

    print("Time now is : ", datetime.datetime.now())

    ## First - get object size distribution
    sz  = obj_size("./", "subtrace.txt.sizeCntObj.json")
    sizes = sz.get_objects(10 * no_objects)
    plot_list(sizes, "sampled")
    plt.grid()
    plt.legend()
    plt.savefig("size_dst.png")    
    plt.clf()

    print("Read the size distribution ", "max_obj_sz : ", max(sizes))
    print("Time now is : ", datetime.datetime.now())        

    ## Get the Footprint descriptor
    fd = FD("./", "sfd_bytes.txt")
    print("Parsed footprint descriptor")
    print("Time now is : ", datetime.datetime.now())

    ## generate a random trace
    trace = range(no_objects)

    f = open("sampled_sizes_" + str(del_rate) + ".txt", "w")
    for s in sizes:
        f.write(str(s) + "\n")
    f.close()

    sampled_fds = np.random.choice(fd.sds, 1.5*t_len, p=fd.sds_pdf)
    sampled_fds = [int(x)/sc_fd for x in sampled_fds]
    sampled_fds = [x for x in sampled_fds if x != 0]

    print("max sampled sds : ", max(sampled_fds[:t_len/2]), max(fd.sds), len(sampled_fds))

    f = open("sampled_sds_" + str(del_rate) + ".txt", "w")
    for s in sampled_fds:
        f.write(str(s) + ",")
    f.close()
    
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
    curr_objects = no_objects

    f2 = open("success_" + str(del_rate) + ".txt", "w")
    
    random_numbers = np.random.rand(10000)
    count_j = 0

    while curr != None and i < 1.5*t_len:
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
        if random_numbers[count_j] < del_rate:
            end_object = True

        if end_object == False:        
            descrepency = root.insertAt(sd, n, 0, curr.id)                
            descs[descrepency] += 1
            if n.parent != None :
                n.parent.rebalance()    
        else :
            n = node(curr_objects, sizes[curr_objects])
            curr_objects += 1
            n.set_b()
            descrepency = root.insertAt(root.s - 1, n, 0, curr.id)
            if n.parent != None:
                n.parent.rebalance()        
        count_j += 1
    
        next, success = curr.findNext()
        while (next != None and next.b == 0) or success == -1:
            next, success = next.findNext()

        del_nodes = curr.cleanUpAfterInsertion(sd, n)        

        if i % 10000 == 0:
            print("Trace computed : ", i, datetime.datetime.now(), root.s)
            count_j = 0
            random_numbers = np.random.rand(10000)

        f2.write(str(sd) + ",")        
        curr = next
        i += 1
            
    print("Number of descrepencies : ", no_desc)

    print("Number of failures : ", fail)
    #max_obj_sz = max(sizes)
    #pop = obj_pop("../gypsum_code/", "sub_pop_dst2.json")        
    #pop.assign_popularities(sz)
    #print("Read the popularity distribution")
    #th_cdf, th_d_vals, th_ = pop.getDelta(sizes ,-max_obj_sz, max_obj_sz, sc)
    #plt.plot(th_d_vals, th_cdf, label="theory")       
    plot_dict(descs)
    plt.savefig("descs_" + str(del_rate) +".png")
    plt.clf() 
    
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

    plot_list(sampled_fds)
    plt.plot(sds2, fd2, label="alg")
    plt.grid()
    plt.legend()
    plt.savefig("fd_compare_" + str(del_rate) + ".png")

    f = open("out_trace_" + str(del_rate) + ".txt", "w")
    for i,o in enumerate(c_trace):
        try :
            if c_trace[i+1] == c_trace[i]:
                continue
        except:
            pass
        f.write(str(o))
        f.write(",")        
    f.close()


