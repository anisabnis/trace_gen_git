f = open("v/out_trace_all.txt", "r")
l = f.readline()
reqs = l.strip().split(",")[:-1]
reqs = [int(x) for x in reqs]
f.close()


f = open("v/sampled_sizes_all.txt", "r")
l = f.readline()
sizes = l.strip().split(",")[:-1]
sizes = [int(x) for x in sizes]
f.close()

byt = 0
for r in reqs:
    byt += sizes[r]

print(float(byt)/len(reqs))
