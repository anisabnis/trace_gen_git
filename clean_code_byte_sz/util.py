from treelib import *
from gen_trace import *
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt


def plot_dict(x, label="-"):
    keys = list(x.keys())
    keys.sort()

    vals = []
    for k in keys:
        vals.append(x[k])
    
    sum_vals = sum(vals)
    vals = [float(x)/sum_vals for x in vals]
    vals = np.cumsum(vals)
    
    plt.plot(keys, vals, label=label)#, marker="^", markersize=3, markevery=500)


def plot_list(x, label="-", maxlim=100000000000):
    a = defaultdict(int)
    for v in x:
        if v < maxlim:
            a[v] += 1

    plot_dict(a, label)


def gen_sd_dst(trace, sizes, scale, stop, log_file, debug):
    trace_list = gen_leaves(trace, sizes)
    st_tree, lvl = generate_tree(trace_list)

    root = st_tree[lvl][0]
    curr = st_tree[0][0]

    log_file.write("Root.s in the generated trace : " +  str(root.s) + "\n")

    fd = defaultdict(int)

    max_sd = 0

    i = 0
    while curr != None:

        curr_next = curr.next
        
        if curr_next == None:
            pass
            #debug.write("uniq bytes " + str(-1) + "\n")
        else:
            uniq_bytes = curr.findUniqBytes(curr_next, log_file) + curr.s
            debug.write("uniq bytes " + str(uniq_bytes) + "\n")
            uniq_bytes = int(float(uniq_bytes)/scale) * scale
            fd[uniq_bytes] += 1
            curr_next.set_b()
            curr_next.update_till_root()
            
            if uniq_bytes > max_sd:
                max_sd = uniq_bytes

        
        ## delete curr and reduce the tree value
        next_node = curr.findNext() 
        next_node = next_node[0]
        curr.delete_node(log_file)
        curr = next_node
        i += 1

        if i%50000 == 0:
            log_file.write("iter : " + str(i) + "\n")
            log_file.flush()
            print("iter : " + str(i))

        if i > stop:
            break
                
    uniq_keys = list(fd.keys())
    uniq_keys.sort()
    vals = []
    for u in uniq_keys:
        vals.append(fd[u])
    sum_vals = sum(vals)
    vals = [float(x)/sum_vals for x in vals]
    vals_cdf = np.cumsum(vals)

    return vals_cdf, vals, uniq_keys, max_sd

        
    


