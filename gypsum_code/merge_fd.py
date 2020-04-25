import sys
import numpy as np
from collections import defaultdict

dir = "/mnt/nfs/scratch1/asabnis/data/binary/"
f1 = dir + sys[1] + "/Fd.txt"
f2 = dir + sys[2] + "/Fd.txt"

max_sd = 0

first_fd = defaultdict(float)
fd1 = open(f1, "r")
for l in fd1:
    l = l.strip().split(" ")
    fd = int(l[0])
    p  = float(l[1])
    first_fd[fd] = p
    
    if fd > max_sd:
        max_sd = fd

second_fd = defaultdict(float)
fd2 = open(f2, "r")
for l in fd2:
    l = l.strip().split(" ")
    fd = int(l[0])
    p  = float(l[1])
    second_fd[fd] = p

    if fd > max_sd:
        max_sd = fd


sd1 = []
sd2 = []

for sd in list(range(200, max_sd, 200)):
    if sd in first_fd:
        sd1.append(first_fd[sd])
    else:
        sd1.append(0)

    if sd in second_fd:
        sd2.append(second_fd[sd])
    else:
        sd2.append(0)

