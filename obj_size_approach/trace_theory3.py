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

exp_number = sys.argv[1]

if not os.path.exists(exp_number):
    os.makedirs(exp_number)


def main2(alpha):

    total_objects = 1000
    length_trace = 100000
    max_obj_sz = 100

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
    t_delta, t_vals, t_delta_pdf = pop.getDelta(objects, -1 * (max_obj_sz - 1), (max_obj_sz-1)) 

    print("t_delta_pdf : ", t_delta_pdf, sum(t_delta_pdf))

    t_delta_req = t_delta_pdf + [0] * (len(sfd1) - int(len(t_delta_pdf)/2))
    
    J = list(range(len(sfd1)))            
    J.reverse()
    X = []
    #sys.exit()

    print(t_delta_req)
    
    print("len(sfd) : ", len(sfd1))

    for j in J:
        sum_1 = 0
        k = len(X)

        #print("sfd[j] : ", sfd1[j], "t_delta_req[k] ", t_delta_req[k])

        for i in range(len(X)):
            sum_1 += (t_delta_req[k] * X[i])

            #print("t_delta_req[k] ", "X[i] ", t_delta_req[k], X[i])

            k = k - 1

        if t_delta_pdf[k] == 0:            
            x_j = (sfd1[j] - sum_1)
        else:
            x_j = float(sfd1[j] - sum_1)/t_delta_pdf[k]

        #print("x_j : ", x_j)

        X.append(x_j)

        if len(X) >= len(sfd1) - int(len(t_delta_pdf)/2):
            break

    print("sum_x : ", sum(X))
    t_delta_1 = t_delta_pdf[:int(len(t_delta_pdf)/2)+1]
    t_delta_1.reverse()
    t_delta_1 = t_delta_1 + [0] * (len(sfd1) - len(t_delta_1) -  int(len(t_delta_pdf)/2))    
    t_delta_2 = t_delta_pdf[int(len(t_delta_pdf)/2):]   
    t_delta_2 = t_delta_2 + [0] * (len(sfd1) - len(t_delta_2) -  int(len(t_delta_pdf)/2))

    Q = toeplitz(t_delta_1, t_delta_2)
    last_row = Q[-1]
    iter = int(len(t_delta_pdf)/2)
    Q_ = []
    
    for i in range(iter):
        last_row = last_row[:-1]
        last_row = np.insert(last_row, 0, 0)
        Q_.append(last_row)
        #Q = np.vstack((Q, last_row))

    Q_ = np.array(Q_)
    Q = np.vstack((Q, Q_))
    res = np.dot(Q, X)
    for i in range(len(res)):
        print(res[i], sfd1[i])
    
    #plt.clf()
    #plt.plot(sds2, fd2, label="Alg")
    plt.plot(sds1, fd, label="orig")
    #plt.plot(sds3, fd3, label="lstsq")

    #plt.legend()
    plt.savefig(exp_number + "/Fd_compare.png")


    
if __name__ == "__main__":

    for alpha in [0.8]:
        for i in [1]:
            main2(alpha)
