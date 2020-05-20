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
import cvxopt

exp_number = sys.argv[1]

if not os.path.exists(exp_number):
    os.makedirs(exp_number)


def main2(alpha):

    total_objects = 500
    length_trace = 20000
    max_obj_sz = 2000

    sc = 1
    obj_dst = obj_size_uniform(1, max_obj_sz)    
    objects, dst = obj_dst.get_objects(total_objects)

    pop = PopularityDst(alpha)
    pop.assignPopularities(objects)
    #t_delta, t_vals, t_delta_pdf = pop.getDelta(objects, -10000, 10000) 

    #fd, sfd1, sds1 = gen_step_fd()
    print("Generating 1st trace according to popularity distribution")
    trace, loc_frac, object_sizes = pop.get_trace(objects, length_trace)    
    print("Generating stack distance dst")
    fd, sfd1, sds1 = gen_fd(trace, objects, "fd1", sc)

    ###############################################

    sc = 1
    obj_dst = obj_size_uniform(1, max_obj_sz)    
    objects, dst = obj_dst.get_objects(total_objects)
    t_delta, t_vals, t_delta_pdf = pop.getDelta(objects, -1 * max_obj_sz, max_obj_sz) 

    print("generating a new trace")
    trace, loc_frac1, object_sizes1 = pop.get_trace(objects, length_trace)    
    trace, p_vals, p_delta, sizes, dst_simple, s_vals, s_dst, fall_dst = generate_trace3(fd, objects, trace, sds1, sc)
    fd2, sfd2, sds2 = gen_fd(trace, objects, "fd2", sc)
    plt.clf()

    t_delta_1 = t_delta_pdf[:int(len(t_delta_pdf)/2)+1]
    t_delta_1.reverse()
    t_delta_1 = t_delta_1 + [0] * (len(sfd1) - len(t_delta_1))    
    t_delta_2 = t_delta_pdf[int(len(t_delta_pdf)/2):]   
    t_delta_2 = t_delta_2 + [0] * (len(sfd1) - len(t_delta_2))

#    Q = toeplitz(t_delta_1, t_delta_2)
#     last_row = Q[-1]
#     iter = int(len(t_delta_pdf)/2)
#     Q_ = []
    
#     print(iter)
#     for i in range(iter):
#         last_row = last_row[:-1]
#         last_row = np.insert(last_row, 0, 0)
#         Q_.append(last_row)
#         print(i)
#         #Q = np.vstack((Q, last_row))

#     Q_ = np.array(Q_)
#     Q = np.vstack((Q, Q_))

#     print("built Q")
#     #X = nnls(Q, sfd1)[0]

#     print("shapes : ", Q.shape, len(sfd1))
    
#     X = nnls(Q, sfd1)
#     obj = X[1]
#     X = X[0]
#     print("objective : ", sum(X), len(X), obj)
#     for x in X:
#         print(x)
#     sum_x = sum(X)

#     X = [float(x)/sum_x for x in X]
#     X = np.cumsum(X)

#     plt.plot(sds1, X, label="X")
#     plt.plot(sds1, fd, label="orig")
#     plt.plot(sds2, fd2, label="alg")

#     res = np.dot(Q, X)
#     print("lengths")
#     print(len(res), len(sfd1))
#     for i in range(len(res)):
#         print(res[i], sfd1[i])
    

#     print("sum_x : ", sum(X))

#     X = np.cumsum(X)    
#     trace, loc_frac1, object_sizes1 = pop.get_trace(objects, length_trace)    
#     trace, p_vals, p_delta, sizes, dst_simple, s_vals, s_dst, fall_dst = generate_trace3(X, objects, trace, sds1, sc)
#     fd3, sfd3, sds3 = gen_fd(trace, objects, "fd2", sc)

#     X = np.cumsum(X)

#     r_fd = np.convolve(sfd1, t_delta_pdf, 'same')
#     r_fd = np.cumsum(r_fd)


#     plt.clf()
#     plt.plot(sds2, fd2, label="Alg")
#     plt.plot(sds1, fd, label="orig")
#     plt.plot(sds3, fd3, label="lstsq")

#     plt.plot(sds1, r_fd[:len(sds1)], label="pred")
#     plt.plot(sds1[:len(X)], X, label="Sample")
#    plt.plot(sds3, fd3, label="fft")
    
    plt.legend()
    plt.savefig(exp_number + "/Fd_compare.png")
#     plt.clf()


    
if __name__ == "__main__":

    for alpha in [0.8]:
        for i in [1]:
            main2(alpha)
