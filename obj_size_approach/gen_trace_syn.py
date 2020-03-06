import sys
from sd import *
import bisect
from collections import defaultdict
from obj_size_dst import *
from noise import *
import copy
import matplotlib.pyplot as plt
import random

fd_name = sys.argv[1]
no_objects = int(sys.argv[2])
trace_len = int(sys.argv[3])

def parseFD(fd_name):
    f = open(fd_name, "r")
    
    fd = defaultdict(list)

    for l in f:

        l = l.strip(" ").split()
        iat = int(l[0])
        sd = int(l[1])
        pr = float(l[2])
        bisect.insort(fd[iat], (sd, pr))                        

    use_fd = defaultdict(list)

    for t in fd:
        if len(fd[t]) > 0:
            use_fd[t] = fd[t]
        else:
            print("fd[t] : ", fd[t])

    return use_fd


def genArbitFD():
    sum = 0
    fd = defaultdict(list)

    for i in range(100):
        fd_pr = random.randint(1,50)
        sum += fd_pr
        fd[100].append((100*i, fd_pr))

    fd[100] = [(x[0],float(x[1])/sum) for x in fd[100]]
    return fd        



def generate_trace(sd, obj_sizes):

    trace_prop = defaultdict(lambda : [])

    all_objects = list(obj_sizes.keys())
    all_objects.sort()

    object_hit_dst = defaultdict(lambda : 0)

    trace = []
    for i in range(trace_len):
        trace.append(random.choice(all_objects))

    for i in range(trace_len):

        if i%1000 == 0:
            print("generating trace : ", i)

        try :
            curr_item = trace[i]
            
        #s = sd.sampleSD()
            s = 4000
            j = trace[i+1:].index(curr_item)
            j = i + j
            
            o_size = obj_sizes[trace[i]]

            uniq_ele = set()
            uniq_bytes = 0        
            
            success = False

            for k in range(i+1, len(trace)):

                if trace[k] == curr_item:
                    trace = trace[:k] + trace[k+1:]                
                else:
                    if trace[k] not in uniq_ele:
                        uniq_bytes += obj_sizes[trace[k]]
                        uniq_ele.add(trace[k])
                        
                    if uniq_bytes > s:
                        success = True
                        break

            if success == True:
                threshold = float(uniq_bytes - s)/o_size
                z = random.random()
                if z < threshold:
                    k = k - 1
                    uniq_bytes -= obj_sizes[trace[k]]


            object_hit_dst[trace[k]] += 1
            trace = trace[:j] + trace[j+1:]
            trace.insert(k, curr_item)                                
            trace_prop[s].append(uniq_bytes)

        except:
            pass

    return trace, trace_prop, object_hit_dst


def main():

    ## Parse footprint descriptor
    #fd = parseFD(fd_name)

    fd = genArbitFD()

    ## Compute stack distance distribution
    SD = sd(fd)
        
    ## Obj size dst
    obj_dst = obj_size("data/akamai1.bin.sizeCntObj.json")
    
    object_sizes = defaultdict(lambda : 0)    

    for i in range(no_objects):
        sz= random.randint(1, 100)#obj_dst.sample()
        object_sizes[sz] += 1

    all_sizes = list(object_sizes.keys())
    count = []
    all_sizes.sort()

    for a in all_sizes:
        count.append(object_sizes[a])
    sum_count = sum(count)

    obj_sizes = all_sizes 
    size_dst = [float(c)/sum_count for c in count]
    objects = range(len(obj_sizes))
    sz_dict = defaultdict(lambda : 0)

    o_sizes = copy.deepcopy(obj_sizes)
    o_sizes.sort()
    plt.plot(o_sizes)
    plt.savefig("obj_sz_dst.png")
    
    for i in range(len(obj_sizes)):
        sz_dict[i] = obj_sizes[i]
        
    nn = noise(SD, obj_sizes, size_dst)
    nn.modelNoise()
    
    trace, trace_prop, obj_hit_dst = generate_trace(SD, sz_dict)

    trace_count = defaultdict(lambda : 0)
    for t in trace_prop[4000]:
        trace_count[t] += 1
    trace_keys = list(trace_count.keys())
    trace_keys.sort()
    trace_vals = []
    for t in trace_keys:
        trace_vals.append(trace_count[t])
    sum_vals = sum(trace_vals)
    trace_vals = [float(t)/sum_vals for t in trace_vals]    
    plt.clf()
    plt.plot(trace_keys, trace_vals)
    plt.xlabel("stack_distance")
    plt.ylabel("Count")
    plt.savefig("stack_distance.png")


    allvals = list(obj_hit_dst.keys())
    allvals.sort()
    plot_vals = []
    for a in allvals:
        plot_vals.append(obj_hit_dst[a])

    sum_vals = sum(plot_vals)
    plt_vals = [float(x)/sum_vals for x in plot_vals]

    plt.clf()
    plt.plot(allvals, plt_vals)
    plt.savefig("ObjInWay_2.png")
        

        
        


    

if __name__ == "__main__":
    main()
