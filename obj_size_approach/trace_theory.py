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
from util_theory import *
import numpy
import scipy
from scipy.optimize import linprog
import os

exp_number = sys.argv[1]

if not os.path.exists(exp_number):
    os.makedirs(exp_number)


def main2(alpha):

    total_objects = 8000
    length_trace = 100000

    sc = 1
    obj_dst = obj_size_uniform(10, 400)    
    objects, dst = obj_dst.get_objects(total_objects)


    pop = PopularityDst(alpha)
    pop.assignPopularities(objects)
    t_delta, t_vals = pop.getDelta(objects) 
    fd, sfd1, sds1 = gen_step_fd()

    trace, loc_frac, object_sizes = pop.get_trace(objects, length_trace)    
    trace, p_vals, p_delta, sizes, dst_simple, s_vals, s_dst, fall_dst = generate_trace3(fd, objects, trace, sds1, sc)
    

    ## Noise error
    plt.plot(t_vals, t_delta, label="theory")
    plt.plot(p_vals, p_delta, label="practice")
    plt.grid()
    plt.legend()
    plt.savefig(exp_number + "/NoiseError.png")
    plt.clf()
        
    ## Fall_dst        
    for obj in fall_dst:

        fall_keys = list(fall_dst[obj].keys())
        fall_keys.sort()
        fall_vals = []

        for k in fall_keys:
            fall_vals.append(fall_dst[obj][k])
            
        sums= sum(fall_vals)
        fall_vals = [float(x)/sums for x in fall_vals]
        fall_vals = np.cumsum(fall_vals)
        plt.clf()
        plt.plot(fall_keys, fall_vals)
        plt.savefig(exp_number + "/fall" + str(obj) + ".png")


    plt.clf()
    ## Obj fall dst
    fall_obj = defaultdict(lambda : 0)
    for i in range(len(sizes)):
        siz = objects[sizes[i]]
        fall_obj[siz] += dst_simple[i]        

    fall_obj_keys = list(fall_obj.keys())
    fall_obj_keys.sort()
    fall_obj_vals = []        

    for obj in fall_obj_keys:
        fall_obj_vals.append(fall_obj[obj])

    sum_vals = sum(fall_obj_vals)

    fall_obj_vals = [float(x)/sum_vals for x in fall_obj_vals]
    fall_obj_vals = np.cumsum(fall_obj_vals)
    plt.plot(fall_obj_keys, fall_obj_vals, marker="o", label="practice")
    plt.plot(object_sizes, loc_frac, marker="x", label="theory")
    plt.savefig(exp_number + "/fall_sz.png")
    plt.clf()


    
if __name__ == "__main__":

    for alpha in [0.8]:
        for i in [1]:
            main2(alpha)
