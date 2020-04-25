from obj_size_dst import *
from popularity import *
from util_theory import *
from trace_prop import *

def main2():

    sc = 1

    trace_prop = traceProp("data_30/sub_trace.txt")

    print("Parsed trace file ")
    objects, p_dst = trace_prop.get_objects()
    fd, sfd1, sds1 = trace_prop.get_sd()

    max_obj_sz = max(objects)

    t_delta, t_vals, t_delta_pdf = trace_prop.getDelta(objects, -1 * max_obj_sz, max_obj_sz, 100) 

    trace = trace_prop.get_random_trace()   
    print("generated random trace")
    trace, p_vals, p_delta, sizes, dst_simple, s_vals, s_dst, fall_dst = generate_trace3(fd, objects, trace, sds1, 1)
    print("generating a trace representative of the FD")
    fd2, sfd2, sds2 = gen_fd(trace, objects, "fd2", sc)
    print("done")

    ## Noise error
    plt.plot(t_vals, t_delta, label="theory")
    plt.plot(p_vals, p_delta, label="practice")
    plt.grid()
    plt.legend()
    plt.savefig("NoiseError.png")
    plt.clf()

    ## Convolution
    r_fd = np.convolve(sfd1, t_delta_pdf, 'same')
    r_fd = np.cumsum(r_fd)

    ## Stack distance 
    plt.plot(sds1, fd, label="original")
    plt.plot(sds1, r_fd[:len(sds1)], label="pred")
    plt.plot(sds2, fd2, label="algorithm")
    plt.legend()
    plt.grid()    
    plt.savefig("Fd_compare.png")
    plt.clf()

main2()
