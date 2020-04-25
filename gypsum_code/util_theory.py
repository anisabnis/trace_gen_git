import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import random
import copy

def gen_fd(trace, sizes, label, sc):
    fd_d = defaultdict(lambda : 0)

    counter = 0

    sc = 100
    for i in range(len(trace)):        
        if i%1000 == 0:
            print("generating fd : ", i)

        uniq_bytes = 0
        curr_item = trace[i]
        uniq_objects = set()
        success = False

        for k in range(i + 1, len(trace)):
            if trace[k] == curr_item:
                #uniq_bytes += sizes[curr_item]
                success = True
                break
            else:
                if trace[k] not in uniq_objects:
                    uniq_bytes += sizes[trace[k]]
                    uniq_objects.add(trace[k])
             

        if success == True:
            key =  int(float(uniq_bytes)/sc) * sc
            fd_d[key] += 1
        else:
            counter += 1


    ks = list(fd_d.keys())
    ks.sort()

    counts = []
    for k in ks:
        counts.append(fd_d[k])

    #ks = [sc * k for k in ks]
        
    sum_counts = sum(counts)
    counts = [float(x)/sum_counts for x in counts]
    
    s_counts = copy.deepcopy(counts)
    
    counts = np.cumsum(counts)
    
    #plt.plot(ks, counts, label=label)
   # plt.savefig("fd.png")

    print("counter : ", counter)
    return counts, s_counts, ks
    

def gen_step_fd():
    ks = []
    counts = []
    for i in range(1,11):
        ks.append(2000*i)
        counts.append(0.1)

    sum_counts = sum(counts)
    counts = [float(c)/sum_counts for c in counts]
    s_counts = copy.deepcopy(counts)
    counts = np.cumsum(counts)
    #plt.plot(ks, counts, label="original")

    return counts, s_counts, ks
        

def sample_fd(sds_prob, sds):
    z = np.random.random()
    
    obj = sds[-1]
    
    for i in range(len(sds)):            
        if sds_prob[i] >= z:
            obj = sds[i]
            break

    return obj


def generate_trace3(sd, obj_sizes, trace, sds, sc):
    
    count = 0
    trace_len = len(trace)    
    delta_dst = defaultdict(lambda : 0)
    obj_sz_dst = defaultdict(lambda : 0)

    print("SC : ", sc)

    i = 0

    fall_count = defaultdict(lambda : defaultdict(lambda : 0))

    samples= defaultdict(lambda :0)

    while i < trace_len:
        i += 1

        if i > len(trace) - 1:
            break

        if i%1000 == 0:
            print("generate trace : ", i)

        curr_item = trace[i]

        uniq_ele = set()
        uniq_bytes = 0

        s = sample_fd(sd, sds) * sc

        #print("sample : ", s)
                
        success = False
        
        del_items = []

        try:
            j = trace[i+1:].index(curr_item)
            j = i + j + 1
        except:
            j = len(trace)
            trace.append(curr_item)
            #continue

        for k in range(i+1, len(trace)):

            if trace[k] == curr_item:
                del_items.append(k)

            elif trace[k] not in uniq_ele:
                uniq_bytes += obj_sizes[trace[k]]
                uniq_ele.add(trace[k])

            if uniq_bytes >= s:
                success = True
                break

        if success == False or k > len(trace) - 1:
            count += 1
            continue

        o_size = obj_sizes[trace[k]]
        obj_sz_dst[trace[k]] += 1

        if success == True:

            threshold = 1 - float(uniq_bytes - s)/o_size
            thr = np.round(threshold, 2)
            thr = 1 - thr

            fall_count[o_size][thr] += 1

            z = random.random()

            if z > threshold:
                uniq_bytes = uniq_bytes - o_size
                k = k - 1

            delta = uniq_bytes - s
            delta_dst[delta] += 1

            no_del = 0
            for pos in del_items:
                trace = trace[:pos-no_del] + trace[pos-no_del+1:]
                no_del += 1
                
            trace.insert(k-no_del+1, curr_item)


    ## This the deltas
    deltas = list(delta_dst.keys())
    deltas.sort()
    counts = []
    for d in deltas:
        counts.append(delta_dst[d])
    sum_counts = sum(counts)
    dst = [float(x)/sum_counts for x in counts]
    dst = np.cumsum(dst)

    ## Repeat for size
    sizes = list(obj_sz_dst.keys())
    sizes.sort()
    counts = []
    for s in sizes:
        counts.append(obj_sz_dst[s])
    sum_counts = sum(counts)
    dst1 = [float(x)/sum_counts for x in counts]
    dst_simple = copy.deepcopy(dst1)
    dst1 = np.cumsum(dst1)

    return trace, deltas, dst, sizes, dst_simple, sizes, dst1, fall_count
