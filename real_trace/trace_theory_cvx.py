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

    total_objects = 10000
    length_trace = int(sys.argv[2])
    max_obj_sz = 15000

    sc = 1
    #obj_dst = obj_size_uniform(1, max_obj_sz)    
    obj_dst = obj_size_three_distribution(100, 200, 5000, 7000, 12000, 15000, 0.6, 0.2, 0.2)
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

    obj_dst = obj_size_three_distribution(100, 200, 5000, 7000, 12000, 15000, 0.6, 0.2, 0.2)
    #obj_dst = obj_size_two_distribution(1,6000,90000,100000, 0.9)
    objects, dst = obj_dst.get_objects(total_objects)
    t_delta, t_vals, t_delta_pdf = pop.getDelta(objects, -1 * max_obj_sz, max_obj_sz, 100) 

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
    f = open(exp_number + "/dim.txt", "w")
    f.write(str(len(t_delta_1)))
    f.close()

#     t_delta_1.reverse()
#     t_delta_1 = t_delta_1 + [0] * (len(sfd1) - len(t_delta_1))    
#     t_delta_2 = t_delta_pdf[int(len(t_delta_pdf)/2):]   
#     t_delta_2 = t_delta_2 + [0] * (len(sfd1) - len(t_delta_2))

#     Q = toeplitz(t_delta_1, t_delta_2)

#     P = matrix(np.dot(Q.T, Q), tc='d')
#     b = matrix(np.array(sfd1), tc='d')

#     residue = np.dot(b.T, b)
    
#     q = matrix(np.dot(Q.T, b), tc='d')
#     q = -1 * q

#     dimension = Q.shape[0]

#     G = matrix(-1 * np.identity(dimension), tc='d')
#     H = matrix(np.zeros(dimension), tc='d')

#     print("dimension : ", dimension)
    
#     A = np.ones(dimension)
#     A = A.reshape(-1, 1).T
#     print("a_shape : ", A.shape)
#     A = matrix(A, tc='d')

#     b = np.array([[1]])
#     b = b.reshape(-1, 1)
#     b = matrix(b, tc='d')

#     sol = solvers.qp(P, q, G, H, A, b)

#     X = sol['x']
#     X = np.cumsum(X)

#     f = open(exp_number + "/objective.txt", "w")
#     f.write(str(sol['primal objective']) + " " + str(residue))
#     f.close()

#     trace, loc_frac1, object_sizes1 = pop.get_trace(objects, length_trace)    
#     trace, p_vals, p_delta, sizes, dst_simple, s_vals, s_dst, fall_dst = generate_trace3(X, objects, trace, sds1, sc)
#     fd3, sfd3, sds3 = gen_fd(trace, objects, "fd2", sc)

    r_fd = np.convolve(sfd1, t_delta_pdf, 'same')
    r_fd = np.cumsum(r_fd)

#     plt.plot(sds1, X, label="X")
#     plt.plot(sds1, fd, label="orig")
#     #plt.plot(sds2, fd2, label="alg")
#     plt.plot(sds3, fd3, label="fft")    
#     plt.legend() 
#     plt.grid()
#     plt.savefig(exp_number + "/Fd_compare_result.png")
#     plt.clf()


    plt.plot(sds1, fd, label="orig")
    plt.plot(sds2, fd2, label="alg")
    plt.plot(sds1, r_fd[:len(sds1)], label="pred")
#     #plt.plot(sds3, fd3, label="fft")    
    plt.legend() 
    plt.grid()
    plt.savefig(exp_number + "/Fd_compare_query.png")
    plt.clf()

    #

    
if __name__ == "__main__":

    for alpha in [0.7]:
        for i in [1]:
            main2(alpha)
