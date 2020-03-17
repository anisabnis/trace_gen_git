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
import scipy
from scipy.optimize import linprog
import os

exp_number = sys.argv[1]

if not os.path.exists(exp_number):
    os.makedirs(exp_number)


def main2(alpha):

    total_objects = 3000
    length_trace = 70000

    sc = 1

    obj_dst = obj_size_uniform(1,1)    
    objects, dst = obj_dst.get_objects(total_objects)

    pop = PopularityDst(alpha)
    pop.assignPopularities(objects)
    t_delta, t_vals, t_delta_pdf = pop.getDelta(objects, -3000, 3000) 

    trace, loc_frac, object_sizes = pop.get_trace(objects, length_trace)    

    orig_trace = copy.deepcopy(trace)

    fd, sfd1, sds1 = gen_fd(trace, objects, "fd1", sc)

    obj_dst = obj_size_uniform(1, 1)    
    objects, dst = obj_dst.get_objects(total_objects)
    
    for kk in range(1):

        trace, loc_frac, object_sizes = pop.get_trace(objects, length_trace)
    
#        trace, deltas, sizes, dst, dst_simple, fall_dst, aa, bb, cc, sample_sd, sample_sd_dst = generate_trace3(fd, objects, trace, sds1, sc)

        trace, p_vals, p_delta, sizes, dst_simple, s_vals, s_dst, fall_dst = generate_trace3(fd, objects, trace, sds1, sc)

        print("len(trace) : ", len(trace))
        
        fd2, sfd2, sds2 = gen_fd(trace, objects, "fd2", sc)

        print("second done ")

        prev_fd = 0
        for i in range(len(fd2)):
            if fd2[i] - prev_fd >= 0.03:
                print(sds2[i])

            prev_fd = fd2[i]

        #r_fd = np.convolve(sfd1, t_delta_pdf)
        #r_fd = np.cumsum(r_fd)

        #plt.plot(sds1, r_fd[:len(sds1)], label="pred")
        #plt.plot(sample_sd, sample_sd_dst, label="samples")
        plt.legend()
        plt.savefig(exp_number + "/Fd_compare.png")
        plt.clf()
    
  #      sizes is object id and dst is distrubtion across obj ids
    #     fall_obj = defaultdict(lambda : 0)
#         for i in range(len(sizes)):
#             siz = objects[sizes[i]]
#             if siz in fall_obj:
#                 fall_obj[siz] += dst_simple[i]
            
#         fall_obj_keys = list(fall_obj.keys())
#         fall_obj_keys.sort()
#         fall_obj_vals = []
        
#         for obj in fall_obj_keys:
#             fall_obj_vals.append(fall_obj[obj])

#         sum_vals = sum(fall_obj_vals)
#         fall_obj_vals = [float(x)/sum_vals for x in fall_obj_vals]
#         fall_obj_vals = np.cumsum(fall_obj_vals)

                             
#         plt.plot(fall_obj_keys, fall_obj_vals, marker="o", markersize=4, label="practice")
#         plt.plot(sizes, dst, label="practice")
#         plt.legend()
#         plt.savefig(exp_number + "/obj_size_fall.png")
#         plt.clf()
        
#         ## Analyse fall distribution
#         for obj in fall_dst:
            
#             fall_keys = list(fall_dst[obj].keys())
#             fall_keys.sort()
#             fall_vals = []
            
#             for k in fall_keys:
#                 fall_vals.append(fall_dst[obj][k])
                
#             sums= sum(fall_vals)
#             fall_vals = [float(x)/sums for x in fall_vals]
#             fall_vals = np.cumsum(fall_vals)
#             plt.clf()
#             plt.plot(fall_keys, fall_vals)
#             plt.savefig(exp_number + "/fall" + str(obj) + ".png")
    
    #trace, sizes, dst, dst_simple = generate_trace3(fd_new, objects, trace, req_sds, sc)

    #fd3, sfd3, sds3 = gen_fd(trace, objects, "fd3", sc)    

    #plt.legend()
    #plt.savefig("Fd_compare.png")
    
    
if __name__ == "__main__":

    #for alpha in [0.6, 0.7, 0.8, 0.9, 1]:
    for alpha in [0.8]:
        for i in [1]:
            main2(alpha)

    #plt.savefig("fall_position.png")
