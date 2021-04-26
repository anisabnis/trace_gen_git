import sys
from collections import defaultdict

GB = 1000000
tc = sys.argv[1]
csize = int(sys.argv[2]) * GB

a = defaultdict(float)
f = open(tc + "/footprint_desc_all.txt", "r")
l = f.readline()
for l in f:
    l = l.strip().split(" ")
    sd = int(l[1])
    pr = float(l[2])
    a[sd] += pr

all_keys = list(a.keys())
all_keys.sort()
total_pr = 0
for sd in all_keys:
    if sd > csize:
        break
    total_pr += a[sd]
print(total_pr)



