from collections import defaultdict
import sys

t_id = int(sys.argv[1])
cache = defaultdict(int)
reqs = 0
u_bytes = 0

f = open("trace_" + str(t_id) + ".txt", "r")
for l in f:
    l = l.strip().split(" ")
    reqs += 1
    obj = int(l[1])
    if obj not in cache:
        u_bytes += float(l[4])/1000
        cache[obj] += 1
        
    if reqs % 1000000 == 0:
        print(reqs, u_bytes)
