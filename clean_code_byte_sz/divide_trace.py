from collections import defaultdict

f = open("all_sort_int", "r")

files = {}

for i in range(20):
    files[i] = open("trace_" + str(i) + ".txt", "w")

for l in f:
    l = l.strip().split(" ")
    tc = int(l[2])

    if tc in files:
        files[tc].write(" ".join([str(x) for x in l]))
        files[tc].write("\n")
    

