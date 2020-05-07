from treelib import *
from gen_trace import *
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt


def plot_dict(x):
    keys = list(x.keys())
    keys.sort()

    vals = []
    for k in keys:
        vals.append(x[k])
    
    sum_vals = sum(vals)
    vals = [float(x)/sum_vals for x in vals]
    vals = np.cumsum(vals)
    
    plt.plot(keys, vals)


def plot_list(x):
    a = defaultdict(int)
    for v in x:
        a[v] += 1

    plot_dict(a)


def gen_sd_dst(trace, sizes, scale, stop):
    trace_list = gen_leaves(trace, sizes)
    st_tree, lvl = generate_tree(trace_list)

    root = st_tree[lvl][0]
    curr = st_tree[0][0]

    fd = defaultdict(int)

    i = 0
    while curr != None:

        curr_next = curr.next
        
        if curr_next == None:
            #fd[0] += 1
            pass
        else:
            ## Remember to correct this - uncomment curr.s !!!!!!
            uniq_bytes = curr.findUniqBytes(curr_next) + curr.s
            fd[(int(uniq_bytes)/scale) * scale] += 1
            curr_next.set_b()
            
            p = curr_next.parent
            add_val = curr_next.s * curr_next.b

            while p != None:
                p.s += add_val
                p = p.parent

        
        ## delete curr and reduce the tree value
        next_node = curr.findNext() 
        next_node = next_node[0]
        curr.delete_node()
        curr = next_node
        i += 1

        if i%1000 == 0:
            print("iter : ", i)

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

    return vals_cdf, vals, uniq_keys

        
    


