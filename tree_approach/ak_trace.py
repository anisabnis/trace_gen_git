import sys
from treelib import *
from collections import defaultdict
from gen_trace import *
from obj_size_dst import *
from obj_pop_dst import *
from parse_fd import *
import datetime


if __name__ == "__main__":
    
    t_len = int(sys.argv[1])
    no_objects = int(sys.argv[2])
    sc = 100000
    
    print("Time now is : ", datetime.datetime.now())

    ## First - get object size distribution
    sz  = obj_size("../gypsum_code/", "akamai1.bin.sizeCntObj.json")
    sz.get_objects(no_objects)
    print("Read the size distribution")
    print("Time now is : ", datetime.datetime.now())        

    ## second - get the popularity distribution
    pop = obj_pop("../gypsum_code/", "sub_pop_dst2.json")        
    pop.assign_popularities(sz)
    print("Read the popularity distribution")
    print("Time now is : ", datetime.datetime.now())

    ## Get the Footprint descriptor
    fd = FD("../gypsum_code/", "st_out")
    print("Parsed footprint descriptor")

    print("Time now is : ", datetime.datetime.now())

    ## generate a random trace
    trace = pop.get_trace(sz, t_len)
    sizes = sz.objects

    #trace = [1,6,4,2,4,3,6,6,7,4,6,7,2,1,0,1]
    #trace = [1, 5, 7, 1, 3, 1, 3, 5, 5, 2, 4, 7, 7, 1, 4, 4]
    #sizes = [10, 25, 10, 36, 11, 46, 10, 41]
    #sizes = [55, 33, 31, 18, 24, 51, 41, 45]

    f = open("sampled_sizes.txt", "w")
    for s in sizes:
        f.write(str(s) + "\n")
    f.close()

    f = open("trace_init.txt", "w")
    for t in trace:
        f.write(str(t) + "\n")
    f.close()
    
    trace_list = gen_leaves(trace, sizes)
    st_tree, lvl = generate_tree(trace_list)
    root = st_tree[lvl][0]
    curr = st_tree[0][0]

    print("size of the root : ", root.s, " and id : ", root.id)

    c_trace = []
    i = 0

    print("------------------")
    print_tree(root)
    print("------------------")

    while curr != None and i < 3*t_len:

        sd = sample(fd.sds, fd.sds_pr)
        sd = int(sd/1000000)
        print("sd :", sd, " curr.s : ", curr.s, " curr.id : ", curr.id, curr.obj_id)

        if sd >= root.s:
            i += 1
            continue

        n  = node(curr.obj_id, curr.s)        
        n.set_b()
        c_trace.append(curr.obj_id)
        
        descrepency = root.insertAt(sd, n, 0, curr.id)                
        ## If the object is going to be inserted right next to it then 
        ## do not insert it there. Come up with a cleaner solution later!
        if descrepency == "Na" :
            continue

        next = curr.findNext()
        while next != None and next.b == 0:
            next = next.findNext()

        print("------------------")
        print("total size under root : ", root.s)
        print_tree(root)
        print("------------------")

        #print("next.id : ", next.id)
        curr.cleanUpAfterInsertion(sd, n)

        #print("Deleting node ", root.s)
        #curr.delete_node()
        print("Deleted node ", root.s)
        n.update_till_root()
        print("Update value from new node ", root.s)

        print("------------------")
        print_tree(root)
        print("------------------")

        if i % 10000 == 0:
            print("Trace computed : ", i, datetime.datetime.now())

        curr = next
        i += 1

    print("Time now is : ", datetime.datetime.now())

    print(c_trace)
            
#     f = open("out_trace.txt", "w")
#     for i,o in enumerate(c_trace):
#         try :
#             if c_trace[i+1] == c_trace[i]:
#                 continue
#         except:
#             pass

#         f.write(str(o) + " " + str(sizes[o]))
#         f.write("\n")        
#     f.close()
