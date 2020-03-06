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


               
def main2(alpha):

    total_objects = 100
    length_trace = 100000

    sc = 1

    obj_dst = obj_size_uniform(1, 20)    
    objects, dst = obj_dst.get_objects(total_objects)
    objects = [sc * x for x in objects]

#     for i in range(len(objects)):
#         #        z = random.random()
#         #        if z < 0.02:
#         if i == 10 or i == 20:
#             objects[i] = 100


    pop = PopularityDst(alpha)
    trace = pop.get_trace(objects, length_trace)
 
    orig_trace = copy.deepcopy(trace)

    fd, sfd1, sds1 = gen_fd(trace, objects, "fd1", sc)

    trace = []
    for i in range(length_trace):
        r_o = random.randint(0,total_objects - 1)
        trace.append(r_o)
    
    trace, sizes, dst, dst_simple, error_k = generate_trace4(fd, objects, trace, sds1, sc)

    fd2, sfd2, sds2 = gen_fd(trace, objects, "fd2", sc)

    print("second done ")
    #plt.legend()
    #plt.savefig("Fd_compare.png")
    #sys.exit()

    A = []
    B = []

    del_rows = []

    req_sds = []

    print("SDS : ", len(sds1))

    #for i in range(len(sfd1)):
    for s in error_k:

        #s = sds1[i]# * 10
        
        errs = list(error_k[s].keys())
        errs.sort()
        err_p = []
        
        a = []
        for e in errs:
            err_p.append(error_k[s][e])

            s1 = e# * 10        
            coeff = 0
            
            for k in range(len(sizes)):
                o = sizes[k]                

                if o >= sc * abs(s - s1):
                    val = 1 - (float(sc * abs(s - s1))/o)
                    #val = 1 - abs(float(s-s1))/(o)
                    val = (val) * (sc/(o + sc))                    
                    val = (val) * dst_simple[k]
                    coeff += val
            
            #coeff = coeff/total_objects
            a.append(coeff)

        sum_err = sum(err_p)
        err_p = [float(x)/sum_err for x in err_p]
        err_p = np.cumsum(err_p)
        sum_a = sum(a)
        a = [float(x)/sum_a for x in a]
        a = np.cumsum(a)
        plt.plot(errs, err_p, label="practice")
        plt.plot(errs, a, label="theory")
        plt.legend()
        plt.savefig("sds/" + str(s) + ".png")
        plt.clf()


#         if sum(a) == 0:
#             del_rows.append(i)
#         else:
#             req_sds.append(sds1[i])

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

#     A_1 = np.ones(np.shape(A_p)[1])
#     S_0 = np.zeros(np.shape(S_p)[1])
    
#     A_1_n = np.negative(A_1)
#     S_0_n = np.negative(S_0)
    

#     ### ------ #####

#     C = np.zeros(np.shape(A_p)[1])
#     C = np.append(C, np.ones(np.shape(S_p)[1]))
    
#     T = np.hstack((A_p, S_n))
#     D = np.hstack((A_n, S_n))
#     E = np.hstack((A_1, S_0))
#     E1 = np.hstack((A_1_n, S_0_n))    

#     B = np.hstack((B_p, B_n))

#     B = np.hstack((B, np.array([1])))
#     B = np.hstack((B, np.array([-1])))
    
#     A = np.vstack((T, D))
#     A = np.vstack((A, E))
#     A = np.vstack((A, E1))
    
    
#     ## We have A, B and C
#     bounds = [(0,1)] * np.shape(A)[1]

#     res = linprog(C, A_ub=A, b_ub=B, options={"disp": True,  'maxiter' : 10000, 'tol' : 0.001}, method='revised simplex')

#     fd_new = res.x[:len(sds1)-no_del]
#     fd_new = np.cumsum(fd_new)

#     trace = []
#     for i in range(length_trace):
#         r_o = random.randint(0,total_objects - 1)
#         trace.append(r_o)

#     #obj_dst = obj_size_uniform(2, 10)    
#     #objects, dst = obj_dst.get_objects(total_objects)
#     #objects = [sc * x for x in objects]

#     plt.plot(fd_new, label="fd_new")
    
#     trace, sizes, dst, dst_simple = generate_trace3(fd_new, objects, trace, req_sds, sc)

#     fd3, sfd3, sds3 = gen_fd(trace, objects, "fd3", sc)    

#     plt.legend()
#     plt.savefig("Fd_compare.png")
    
    
if __name__ == "__main__":

    #for alpha in [0.6, 0.7, 0.8, 0.9, 1]:
    for alpha in [0.9]:
        for i in [1]:
            main2(alpha)

    #plt.savefig("fall_position.png")
