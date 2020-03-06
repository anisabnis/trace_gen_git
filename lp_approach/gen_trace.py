import sys
from iat import *
from sd import *
import bisect
from lp import *

fd_name = sys.argv[1]
no_objects = int(sys.argv[2])
trace_len = int(sys.argv[3])

def parseFD(fd_name):
    f = open(fd_name, "r")
    
    fd = defaultdict(list)

    for l in f:

        l = l.strip(" ").split()
        iat = int(l[0])
        sd = int(l[1])
        pr = float(l[2])
        bisect.insort(fd[iat], (sd, pr))                        

    use_fd = defaultdict(list)

    for t in fd:

        if len(fd[t]) > 0:
            use_fd[t] = fd[t]
        else:
            print("fd[t] : ", fd[t])

    return use_fd


def main():

    ##
    fd = parseFD(fd_name)
    
    ##
    IAT = iat(fd)

    ##
    trace = IAT.genTrace(no_objects, trace_len)

    ##
    SD = sd(fd)
        
    SD.assignSD(trace)

    #for t in trace:
    #    print(t)

    #trace = [[1,1,4,3],[2,2,5,3],[3,3,6,3],[4,1,0,0],[5,2,0,0],[6,3,0,0]]

    LP = lp(trace)

    

    #err, obj_size = LP.solve()
    
    


    

    


if __name__ == "__main__":
    main()
