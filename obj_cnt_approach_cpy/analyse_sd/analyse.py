# f = open("fd_popularity.txt", "r")
# keys = 0
# for l in f:
#     l = l.strip().split(" ")
#     if len(l) == 1:
#         keys += 1

#print(keys)
from joint_dst import *

o = pop_sz_dst("fd_popularity.txt")
