import sys
from sd import *
import bisect
from collections import defaultdict
from obj_size_dst import *
from noise import *
import copy
import matplotlib.pyplot as plt
import random
from popularity import *
from util import *
import numpy
#import scipy
#import scipy.optimize.linprog
from scipy.optimize import linprog

#fd_name = sys.argv[1]
#no_objects = int(sys.argv[2])
#trace_len = int(sys.argv[3])

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
        

        
        
def main2():

    total_objects = 100
    length_trace = 1000


    obj_dst = obj_size_uniform(2, 50)    
    objects, dst = obj_dst.get_objects(total_objects)
    objects = [1000 * x for x in objects]


    pop = PopularityDst(1)
    trace = pop.get_trace(objects, length_trace)
 
    orig_trace = copy.deepcopy(trace)

    fd, sfd1, sds = gen_fd(trace, objects, "fd1")

    print("First done ")

    random.shuffle(trace)

#    obj_dst = obj_size_uniform(2, 50)    
#    objects, dst = obj_dst.get_objects(total_objects)

#    objects = [1000 * x for x in objects]

    trace = []
    for i in range(length_trace):
        r_o = random.randint(0,total_objects - 1)
        trace.append(r_o)
    
    trace, sizes, dst = generate_trace2(fd, objects, trace, sds)

    fd2, sfd2, sds = gen_fd(trace, objects, "fd2")

    print("second done ")

    plt.legend()
    plt.savefig("Fd_compare.png")
    
#    plt.clf()       
#    plt.plot(sizes, dst)
#    plt.savefig("fall.png")

#     A = []
#     B = []
#     print(len(sds))

#     del_rows = []

#     for i in range(len(sds)):
#         s = sds[i]
#         a = []

#         for j in range(len(sds)):
#             s1 = sds[j]        
#             coeff = 0

#             for k in range(total_objects):
#                 o = objects[k]                
#                 o = o/1000

#                 if o > abs(s - s1):
#                     val = float(abs(s - s1))/o
#                     val = (val)/(o+1)                    
#                     coeff += val
            
#             coeff = coeff/total_objects
#             a.append(coeff)

#         if sum(a) == 0:
#             del_rows.append(i)

#         A.append(a)
#         B.append(sfd1[i])

#     A = numpy.array(A)
#     B = numpy.array(B)
#     no_del = 0
#     for i in del_rows:
#         A = np.delete(A, i - no_del, 0)
#         A = np.delete(A, i - no_del, 1) 
#         B = np.delete(B, i - no_del)
#         no_del += 1

#     A_p = copy.deepcopy(A)
#     A_n = np.negative(A_p)

#     B_p = copy.deepcopy(B)
#     B_n = np.negative(B_p)

#     S_p = np.identity(np.shape(A_p)[0])
#     S_n = np.negative(S_p)

#     B_p = copy.deepcopy(B)
#     B_n = np.negative(B_p)

#     A_1 = np.ones(np.shape(A_p)[0])
#     S_0 = np.zeros(np.shape(S_p)[0])
    
#     A_1_n = np.negative(A_1)
#     S_0_n = np.negative(S_0)
    

#     ### ------ #####

#     C = np.zeros(np.shape(A_p)[0])
#     C = np.append(C, np.ones(np.shape(S_p)[0]))
    
#     T = np.hstack((A_p, S_p))
#     D = np.hstack((A_n, S_n))
#     E = np.hstack((A_1, S_0))
#     E1 = np.hstack((A_1_n, S_0_n))    

#     print("Before : ", B_p)
#     B = np.hstack((B_p, B_n))
#     print("B : ", B)

#     B = np.hstack((B, np.array([1])))
#     B = np.hstack((B, np.array([-1])))
    
#     A = np.vstack((T, D))
#     A = np.vstack((A, E))
#     A = np.vstack((A, E1))
    
    
#     ## We have A, B and C
#     bounds = [(0,1)] * np.shape(A)[1]

#     res = linprog(C, A_ub=A, b_ub=B, bounds=bounds, options={"disp": True})

#     print(res)



#    S_p = np.identity
    
    


#    no_cols = A.shape[1]
#    ones = np.ones(no_cols)
    
#    A = np.vstack((A, ones))
#    B = np.append(B, 1)

#    print(A.shape)

    
    
#    x = np.linalg.solve(A, B)


#    A = A[:-1]
#    B = B[:-1]

#    no_ones = len(A[0])
#    a = [1] * no_ones
#    b = 1

#    A.append(a)
#    B.append(b)


 #   for a in A:
 #       print(a)


    
    #print(A)
    #print(B)

    print(x)

    #fd3 = np.cumsum(x[0])
    #print(fd3)
    

    
    



    

if __name__ == "__main__":
    main2()
