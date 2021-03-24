import sys
from collections import defaultdict

d = sys.argv[1]
MIL = 1000000
total_reqs = 0
obj_reqs = defaultdict(lambda : 0)
f = open(d + "/out_trace_pop.txt")
l = f.readline()
l = l.strip().split(",")[:-1]
l = l[50*MIL:]
for r in l:
    obj_reqs[r] += 1
    total_reqs += 1
counter = 0
for o in obj_reqs:
    if obj_reqs[o] == 1:
        counter += 1
save = float(counter)/total_reqs
print("result ohp : ", save)
