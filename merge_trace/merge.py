import gzip
import io
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



dirs = ["Download", "Image", "Media", "Web"]
files = ["184-119.download.int.all.gz", "184-119.image.int.all.gz", "184-119.media.int.all.gz", "184-119.web.int.all.gz"]
traces = [[],[],[],[]]

j = 0
for i in range(3,4):
    dir = "/Data/Logs/All/184-199/" + dirs[i] + "/"

    object_sizes = defaultdict()
    total_bytes = 0
    unique_bytes = 0
    
    f = gzip.open(dir + files[i], 'r')
    for l in f:
        j += 1
        l = l.strip().decode("utf-8")
        l = [int(x) for x in l.split(" ")]
        l.append(i)
        traces[i].append(l)
        #l[2] = np.ceil(l[2]/1000)

        if l[1] not in object_sizes:
            object_sizes[l[1]] = l[2]
            unique_bytes += l[2]
        total_bytes += l[2]
        if j % 10000 == 0:
            print("lines : ", j)
            #break
    f.close()

    print("number of lines :", j, dir)
    print("total objects : ", len(object_sizes.keys()), " unique bytes : ", unique_bytes, " total bytes ", total_bytes)

    #plot_list(object_sizes.vals())
    plot_dict(object_sizes)
    plt.xscale('log')
    plt.savefig("sz_dst.png")
    
# for i in range(4):
#     traces[i].sort()

# indices = [0,0,0,0]
# max_indices = [len(traces[0]), len(traces[1]), len(traces[2]), len(traces[3])]
# total_len = j
# final_trace = []

# i = 0
# while i < j:
#     first = False
#     for k in range(4):
#         if indices[k] < max_indices[k]:
#             if first == False:
#                 min_index = k
#                 first = True
#                 continue
#             elif traces[k][indices[k]] < traces[min_index][indices[min_index]]:
#                 min_index = k

#     final_trace.append(traces[min_index][indices[min_index]])
#     indices[min_index] += 1
#     if i % 100000 == 0:
#         print("traces : ", i)
#     i += 1

# f = open("final_trace.txt" , "w")
# for t in final_trace:
#     t = " ".join([str(x) for x in t])
#     f.write(t)
#     f.write("\n")
# f.close()
            



    

