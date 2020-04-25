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
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.optimize import nnls
from scipy import linalg
import os
from scipy.linalg import toeplitz
from cvxopt import matrix
import cvxopt
from cvxopt import solvers

solvers.options['abstol'] = 0.001

exp_number = sys.argv[1]

if not os.path.exists(exp_number):
    os.makedirs(exp_number)


def main2(alpha):

    total_objects = 3000
    length_trace = int(sys.argv[2])
    max_obj_sz = 100000

    sc = 1
    #obj_dst = obj_size_uniform(1, max_obj_sz)    
    obj_dst = obj_size_three_distribution(100, 200, 5000, 7000, 12000, 15000, 0.7, 0.2, 0.1)
    objects, dst = obj_dst.get_objects(total_objects)

    total_objects = len(objects)

    pop = PopularityDst(alpha)
    pop.assignPopularities(objects)
    #t_delta, t_vals, t_delta_pdf = pop.getDelta(objects, -10000, 10000) 
    #t_delta, t_vals, t_delta_pdf = pop.getDelta(objects, -1 * max_obj_sz, max_obj_sz, 100) 


    #fd, sfd1, sds1 = gen_step_fd()
    print("Generating 1st trace according to popularity distribution")
    trace, loc_frac, object_sizes = pop.get_trace(objects, length_trace)    
    print("Generating stack distance dst")
    fd, sfd1, sds1 = gen_fd(trace, objects, "fd1", sc)

    ###############################################

    sc = 1
    #obj_dst = obj_size_uniform(1, max_obj_sz)    
    #objects, dst = obj_dst.get_objects(total_objects)
    #t_delta, t_vals, t_delta_pdf = pop.getDelta(objects, -1 * max_obj_sz, max_obj_sz) 

    obj_dst = obj_size_three_distribution(100, 200, 5000, 7000, 12000, 15000, 0.7, 0.2, 0.1)
    #obj_dst = obj_size_two_distribution(1,6000,90000,100000, 0.9)
    objects, dst = obj_dst.get_objects(total_objects)

    t_delta, t_vals, t_delta_pdf = pop.getDelta(objects, -10000, 10000, 20) 


    print("generating a new trace")
    trace, loc_frac1, object_sizes1 = pop.get_trace(objects, length_trace)    

    #trace = []
#     for i in range(length_trace):
#         r_o = random.randint(0,total_objects - 1)
#         trace.append(r_o)
    
    trace, p_vals, p_delta, sizes, dst_simple, s_vals, s_dst, fall_dst = generate_trace3(fd, objects, trace, sds1, sc)
    #trace = trace[:length_trace]
    fd2, sfd2, sds2 = gen_fd(trace, objects, "fd2", sc)
    plt.clf()


    #Noise error
    plt.plot(t_vals, t_delta, label="theory")
    plt.plot(p_vals, p_delta, label="practice")
    plt.grid()
    plt.legend()
    plt.savefig(exp_number + "/NoiseError.png")
    plt.clf()

    t_delta_1 = t_delta_pdf[:int(len(t_delta_pdf)/2)+1]
    t_delta_1.reverse()
    t_delta_1 = t_delta_1 + [0] * (len(sfd1) - len(t_delta_1))    
    t_delta_2 = t_delta_pdf[int(len(t_delta_pdf)/2):]   
    t_delta_2 = t_delta_2 + [0] * (len(sfd1) - len(t_delta_2))

    Q = toeplitz(t_delta_1, t_delta_2)
    np.savetxt(exp_number + "/Q.txt", Q, delimiter=',')

    print("Determinant : ", np.linalg.det(Q))
    
if __name__ == "__main__":

    for alpha in [0.7]:
        for i in [1]:
            main2(alpha)
