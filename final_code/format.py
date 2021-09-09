import sys

directory = sys.argv[1]
type = sys.argv[2]

f = open("results/" + directory + "/footprint_desc_all.txt", "r")
l = f.readline()
l = l.strip().split(" ")
byte_rate = float(l[1])
byte_rate = byte_rate/(float(l[3]) - float(l[2]))
f.close()

reqs = open("results/" + directory + "/out_trace_all.txt", "r")
l = reqs.readline()
rs = l.strip().split(",")
rs = rs[:-1]
rs = [int(x) for x in rs]
reqs.close()

sizes = open("results/" + directory + "/sampled_sizes_all.txt", "r")
l = sizes.readline()
ss = l.strip().split(",")
ss = ss[:-1]
ss = [float(x) for x in ss]
sizes.close()

bytes_added = 0
tm = str(0)
f = open("results/" + directory + "/req_trace.txt", "w")
i = 0
for r in rs:
    f.write(tm + " " + str(r) + " " + str(round(ss[r],2)) + "\n")
    bytes_added += ss[r]
    if bytes_added > byte_rate:
        tm = str(int(tm) + 1)
        bytes_added = 0
    i += 1
    if i % 1000000 == 0:
        print("parsed : "+ str(i))
f.close()
    
    


