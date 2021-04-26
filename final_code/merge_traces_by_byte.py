import sys
import random
from collections import defaultdict

def computeUniqByteRate(f_name):
    f = open(f_name, "r")
    l = f.readline()

    hitrate = defaultdict(lambda: defaultdict(float))

    total_pr = 0
    for l in f:
        l = l.strip().split(" ")
        iat = int(l[0])
        sd = int(l[1])
        pr = float(l[2])
        total_pr += pr
        hitrate[iat][sd] = pr

    ubrate = 0
    for iat in hitrate.keys():
        for sd in hitrate[iat].keys():
            tmp = float(hitrate[iat][sd])/total_pr
            ubrate += (float(sd)/iat)*tmp

    return ubrate
    

dir = sys.argv[1]
tc1 = int(sys.argv[2])
tc2 = int(sys.argv[3])

f1 = open("results/" + str(dir) + "/footprint_desc_" + str(tc1) + ".txt")
l = f1.readline()
l = l.strip().split(" ")
time_delta = int(l[3]) - int(l[2])
br1 = int(float(l[1])/time_delta)
br1 = float(br1)
f1.close()

f2 = open("results/" + str(dir) + "/footprint_desc_" + str(tc2) + ".txt")
l = f2.readline()
l = l.strip().split(" ")
time_delta = int(l[3]) - int(l[2])
br2 = int(float(l[1])/time_delta)
br2 = float(br2)
f2.close()

print(br1, br2)

trace1 = open("results/" + str(dir) + "/out_trace_" + str(tc1) + ".txt")
l1 = trace1.readline().strip()
t1 = l1.split(",")[:-1]
trace1.close()
s1 = open("results/" + str(dir) + "/sampled_sizes_" + str(tc1) + ".txt")
l1 = s1.readline().strip()
sizes1 = l1.split(",")[:-1]


trace2 = open("results/" + str(dir) + "/out_trace_" + str(tc2) + ".txt")
l1 = trace2.readline().strip()
t2 = l1.split(",")[:-1]
trace2.close()
s2 = open("results/" + str(dir) + "/sampled_sizes_" + str(tc2) + ".txt")
l2 = s2.readline().strip()
sizes2 = l2.split(",")[:-1]

f = open("results/" + str(dir) + "/merge_" + str(tc1) + str(tc2) + "by_byte.txt", "w")
i1 = 0
i2 = 0
i = 0
while True:

    try:
        all_reqs = []        
        b1 = 0
        while b1 < br1:
            all_reqs.append([i, str(t1[i1])+":"+str(tc1), sizes1[int(t1[i1])]])
            b1 += int(sizes1[int(t1[i1])])
            i1 += 1
            
        b2 = 0        
        while b2 < br2:
            all_reqs.append([i, str(t2[i2])+":"+str(tc2), sizes2[int(t2[i2])]])
            b2 += int(sizes2[int(t2[i2])])
            i2 += 1

        #random.shuffle(all_reqs)
        for m in all_reqs:
            f.write(str(m[0]) + " " + str(m[1]) + " " + str(m[2]) + "\n")
            
        i += 1
        if i%100000 == 0:
            print(" i : ", i)
    except:
        break

f.close()
