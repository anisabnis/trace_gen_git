import sys
import matplotlib.pyplot as plt
from collections import defaultdict

tc = sys.argv[1]
#f = open("trace_" + tc + ".txt", "r")
f = open("all_sort_int", "r")
l = f.readline()
l = l.strip().split(" ")
ctime = int(l[0])
no_reqs = 0
reqs = []
no_hrs = 0
objs = set()

popularity = defaultdict(int)

for l in f:

    l = l.strip().split(" ")
    t = int(l[0])
    no_reqs += 1
    objs.add(str(int(l[1])) + ":" + str(int(l[2])))

    if t - ctime > 3600:
        ctime = t
        reqs.append(no_reqs)
        no_reqs = 0
        no_hrs += 1

    if no_hrs > 240:
        break

f.close()


print("length of requests : ", sum(reqs), " no of objects : ", len(objs))

f = open("results/" + str(tc) + "/req_hr.txt", "w")
for r in reqs:
    f.write(str(r) + "\n")
f.close()

plt.plot(reqs[72:240])
plt.grid()
plt.xlabel("hrs")
plt.ylabel("No requests")
plt.savefig("all_reqs.png")
    
    
