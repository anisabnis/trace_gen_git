import matplotlib.pyplot as plt
import sys
import numpy as np

eps = sys.argv[1]

f = open("res_fd_" + eps + ".txt", "r")
fds = []
fd_prob = []
i = 0
stop_index = i
for l in f:
    l = l.strip().split(" ")
    fds.append(int(l[0]))
    fd_prob.append(float(l[1]))
    i += 1

    if int(l[0]) > 10000000:
        stop_index = i
        break

f.close()

fds1 = []
fds1_prob = []
i = 0
f = open("sfd_bytes.txt", "r")
for l in f:
    l = l.strip().split(" ")
    fds1.append(int(l[0])/1000)
    fds1_prob.append(float(l[1]))
    i += 1
    
    if int(l[0]) > 10000000000:
        stop_index1 = i
        break
f.close()

fds1_prob = np.cumsum(fds1_prob)
plt.plot(fds, fd_prob, label="alg")
plt.plot(fds1, fds1_prob, label="orig")
plt.xlabel("Stack Distance (KB)")
plt.ylabel("CDF")
plt.grid()
plt.legend()
plt.savefig("fd_" + str(eps) + "_partial.png")    
    
    
