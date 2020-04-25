from util import *
from obj_size_dst import *
from obj_pop_dst import *
from parse_fd import *
import sys

class TraceGen:
    def __init__(self, sz, pop, t_len, sc, fd):
        trace = pop.get_trace(sz, t_len)
        self.fd1, self.sfd1, self.sds1 = gen_fd(trace, sz.objects, sc)

        n_trace, p_vals, p_delta, sizes, dst_simple, s_dst, fall_dst = generate_trace3(self.sds_pr, self.sds, sz.objects, trace)
        self.fd2, self.sfd2, self.sds2 = gen_fd(n_trace, sz.objects, sc)

        #t_delta, t_vals, t_delta_pdf = pop.getDelta(sz.objects, -1 * sz.objects[-1], sz.objects[-1], 1000)         
        #self.fd3, self.sfd3, self.sds3 = find_adjusted_fd(t_vals, t_delta_pdf)


    def print_fd(self):
        # First print the original fd
        f = open("FD1.txt", "w")
        for i in range(len(self.sds1)):
            f.write(str(self.sds1[i]) + " " + str(self.sfd1[i]) + "\n")
        f.close()

        f = open("FD2.txt", "w")
        for i in range(len(self.sds2)):
            f.write(str(self.sds2[i]) + " " + str(self.sfd2[i]) + "\n")
        f.close()        

    def find_adjusted_fd(self):
        return [[],[],[]]



if __name__ == "__main__":

    t_len = int(sys.argv[1])
    no_objects = int(sys.argv[2])

    sc = 100000

    fd = FD("./", "st_out")
    #sz  = obj_size("/mnt/nfs/scratch1/asabnis/data/binary/small/", "akamai1.bin.sizeCntObj.json")

    ## sz.objects has the object sizes
    sz  = obj_size("./", "akamai1.bin.sizeCntObj.json")
    sz.get_objects(no_objects)
    print("Read the size distribution")

    ## pop.popularities has the objects popularity score
    pop = obj_pop("./", "akamai1.bin.popCntObj.json")        
    pop.assign_popularities(sz)
    print("Read the popularity distribution")

    trace_gen = TraceGen(sz, pop, t_len, sc)
    trace_gen.print_fd()



