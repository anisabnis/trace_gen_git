import random
import sys

dir = sys.argv[1]
tc1 = int(sys.argv[2])
tc2 = int(sys.argv[3])

f1 = open("results/" + str(dir) + "/footprint_desc_" + str(tc1) + ".txt")
l = f1.readline()
l = l.strip().split(" ")
time_delta = int(l[3]) - int(l[2])
rr1 = int(int(l[0])/time_delta)
f1.close()

f2 = open("results/" + str(dir) + "/footprint_desc_" + str(tc2) + ".txt")
l = f2.readline()
l = l.strip().split(" ")
time_delta = int(l[3]) - int(l[2])
rr2 = int(int(l[0])/time_delta)
f2.close()

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

f = open("results/" + str(dir) + "/merge_" + str(tc1) + str(tc2) + ".txt", "w")
i = 0
while True:
    try:
        all_reqs = []
        m1 = t1[rr1*i: rr1*(i+1)]
        for m in m1:
            all_reqs.append([str(i), str(m) + ":" + str(tc1), str(sizes1[int(m)])])

        m2 = t2[rr2*i: rr2*(i+1)]
        for m in m2:
            all_reqs.append([str(i),  str(m) + ":" + str(tc2), str(sizes2[int(m)])])

        i += 1

        if i%10000 == 0:
            print("i : ", i)
            
        random.shuffle(all_reqs)

        for a in all_reqs:
            f.write(str(a[0]) + " " + str(a[1]) + " " + str(a[2]) + "\n")

    except:
        break

f.close()
