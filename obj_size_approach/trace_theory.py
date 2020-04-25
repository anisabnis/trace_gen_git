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
from scipy import linalg
import os
from scipy.linalg import toeplitz

exp_number = sys.argv[1]

if not os.path.exists(exp_number):
    os.makedirs(exp_number)


def main2(alpha):

    total_objects = 300
    length_trace = 10000
    max_obj_sz = 600

    sc = 1
    obj_dst = obj_size_uniform(1, max_obj_sz)    
    objects, dst = obj_dst.get_objects(total_objects)

    pop = PopularityDst(alpha)
    pop.assignPopularities(objects)
    #t_delta, t_vals, t_delta_pdf = pop.getDelta(objects, -10000, 10000) 

    #impulse = pop.getImpulse()

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
    #trace, loc_frac1, object_sizes1 = pop.get_trace(objects, length_trace)    
    #trace, p_vals, p_delta, sizes, dst_simple, s_vals, s_dst, fall_dst = generate_trace3(fd, objects, trace, sds1, sc)
    #fd2, sfd2, sds2 = gen_fd(trace, objects, "fd2", sc)

#    Noise error
    #plt.plot(t_vals, t_delta, label="theory")
    #plt.plot(p_vals, p_delta, label="practice")
    #plt.grid()
    #plt.legend()
    #plt.savefig(exp_number + "/NoiseError.png")
    plt.clf()

    print("t_delta L", len(t_delta_pdf), len(sfd1))

    
    #t_delta_pdf = np.concatenate((t_delta_pdf, [0] * (len(sfd1) - len(t_delta))), axis=0)
    #t_delta_pdf = t_delta_pdf + [0]*(len(sfd1) - len(t_delta_pdf))


    t_delta_1 = t_delta_pdf[:int(len(t_delta_pdf)/2)+1]
    t_delta_1.reverse()
    t_delta_1 = t_delta_1 + [0] * (len(sfd1) - len(t_delta_1))
    
    t_delta_2 = t_delta_pdf[int(len(t_delta_pdf)/2):]   
    t_delta_2 = t_delta_2 + [0] * (len(sfd1) - len(t_delta_2))

    print("t_delta_pdf : ", len(t_delta_pdf))

    print("t_Delta 1 : ", t_delta_1)

    print("t_Delta 2 : ", t_delta_2)

    Q = toeplitz(t_delta_1, t_delta_2)
    #Q = Q[1:-5, 1:-5]

    t_delta_new = [0] * len(t_delta_pdf) + t_delta_pdf + [0] * len(t_delta_pdf)
    print(len(sds1))
#     Q = linalg.toeplitz(t_delta_new)
#     Q = Q[:len(t_delta_pdf)]
#     Q = Q[:, len(t_delta_pdf):(2*len(t_delta_pdf))]

    det = np.linalg.matrix_rank(Q)
    f = open("det1.txt", "w")
    f.write("toeplitz done")
    f.flush()
    #det = np.linalg.det(Q)
    
    f.write(str(det))
    f.flush()
    f.close()

    ## First try the matrix multiplication method

#     k = np.fft.fft(sfd1)/np.fft.fft(t_delta_pdf)
#     print("Third : ", k)

#     k2 = np.fft.ifft(k)
#     print("fourth : ", type(k2[1:50])) 
#     plt.clf()
#     fd_fft = k2.real
#     sum_fft = sum(fd_fft)
#     fd_fft = [float(x)/sum_fft for x in fd_fft]

#     plt.plot(sds1, np.cumsum(fd_fft)) 
#     plt.savefig("new_fd.png")

#     fd_fft = np.cumsum(fd_fft)
#     #print(sum( np.fft.ifft(np.fft.fft(fd), np.fft.fft(t_delta_pdf)) ))


#     trace, loc_frac1, object_sizes1 = pop.get_trace(objects, length_trace)    
#     trace, p_vals, p_delta, sizes, dst_simple, s_vals, s_dst, fall_dst = generate_trace3(fd_fft, objects, trace, sds1, sc)
#     fd3, sfd3, sds3 = gen_fd(trace, objects, "fd2", sc)

    ## Fd_compare
    
    #r_fd = np.cumsum(r_fd)
    r_fd = np.convolve(sfd1, t_delta_pdf, 'same')
    r_fd = np.cumsum(r_fd)

    plt.clf()
    #plt.plot(sds2, fd2, label="Alg")
    plt.plot(sds1, fd, label="orig")
    plt.plot(sds1, r_fd[:len(sds1)], label="pred")
    #plt.plot(sds3, fd3, label="fft")
    plt.legend()
    plt.savefig(exp_number + "/Fd_compare.png")
    plt.clf()


    
if __name__ == "__main__":

    for alpha in [0.8]:
        for i in [1]:
            main2(alpha)
